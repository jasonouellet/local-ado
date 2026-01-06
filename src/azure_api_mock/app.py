from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pythonjsonlogger.json import JsonFormatter

from .http_utils import parse_basic_token, parse_bearer_token
from .settings import Settings
from .store import FixtureStore


def _configure_logging() -> None:
    logger = logging.getLogger()
    if logger.handlers:
        return

    handler = logging.StreamHandler()
    formatter = JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def get_settings() -> Settings:
    return Settings()


def get_store(settings: Settings = Depends(get_settings)) -> FixtureStore:
    return FixtureStore.load(settings.fixtures_path)


def require_api_version(
    settings: Settings,
    api_version: str | None,
) -> None:
    if settings.strict_api_version and not api_version:
        raise HTTPException(status_code=400, detail="Missing required query parameter: api-version")
    if api_version and settings.allowed_versions and api_version not in settings.allowed_versions:
        raise HTTPException(status_code=400, detail=f"Unsupported api-version: {api_version}")


def check_auth(settings: Settings, authorization: str | None) -> None:
    mode = (settings.auth_mode or "none").lower()
    if mode == "none":
        return

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token: str | None = None
    if mode == "pat":
        token = parse_basic_token(authorization)
    elif mode == "bearer":
        token = parse_bearer_token(authorization)
    else:
        raise HTTPException(status_code=500, detail=f"Invalid server auth_mode: {settings.auth_mode}")

    if not token:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    if token != settings.token:
        raise HTTPException(status_code=403, detail="Invalid token")


def ado_envelope(items: list[dict[str, Any]], *, count: int | None = None) -> dict[str, Any]:
    return {"count": count if count is not None else len(items), "value": items}


def _apply_top_skip(items: list[dict[str, Any]], top: int | None, skip: int | None) -> list[dict[str, Any]]:
    if skip and skip > 0:
        items = items[skip:]
    if top and top >= 0:
        items = items[:top]
    return items


def create_app() -> FastAPI:
    _configure_logging()
    app = FastAPI(title="azure-api-mock", version="0.1.0")
    log = logging.getLogger("azure-api-mock")

    @app.middleware("http")
    async def correlation_and_logging(request: Request, call_next):
        settings = Settings()

        correlation_id = request.headers.get("x-correlation-id") or str(uuid.uuid4())
        start = time.time()

        if settings.artificial_latency_ms and settings.artificial_latency_ms > 0:
            time.sleep(settings.artificial_latency_ms / 1000.0)

        response: Response
        try:
            response = await call_next(request)
        finally:
            elapsed_ms = int((time.time() - start) * 1000)
            log.info(
                "request",
                extra={
                    "correlation_id": correlation_id,
                    "method": request.method,
                    "path": request.url.path,
                    "query": request.url.query,
                    "elapsed_ms": elapsed_ms,
                },
            )

        response.headers["x-correlation-id"] = correlation_id
        return response

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.get("/__admin/routes")
    def admin_routes():
        out = []
        for r in app.router.routes:
            methods = sorted(getattr(r, "methods", []) or [])
            out.append({"path": getattr(r, "path", None), "methods": methods, "name": getattr(r, "name", None)})
        return {"count": len(out), "value": out}

    @app.get("/__admin/fixtures")
    def admin_fixtures(settings: Settings = Depends(get_settings)):
        store = FixtureStore.load(settings.fixtures_path)
        orgs = sorted((store.data.get("organizations") or {}).keys())
        return {"dataset": settings.dataset, "fixtures_path": settings.fixtures_path, "organizations": orgs}

    # --- Azure DevOps-like endpoints (MVP) ---

    @app.get("/{organization}/_apis/projects")
    def list_projects(
        organization: str,
        request: Request,
        api_version: str | None = None,
        top: int | None = None,
        skip: int | None = None,
        authorization: str | None = Header(default=None),
        settings: Settings = Depends(get_settings),
        store: FixtureStore = Depends(get_store),
    ):
        require_api_version(settings, api_version)
        check_auth(settings, authorization)

        org = store.organization(organization)
        if not org:
            raise HTTPException(status_code=404, detail=f"Organization not found: {organization}")

        projects = list(org.get("projects", []))
        projects = _apply_top_skip(projects, top=top, skip=skip)
        return JSONResponse(ado_envelope(projects))

    @app.get("/{organization}/_apis/projects/{project_id}")
    def get_project(
        organization: str,
        project_id: str,
        api_version: str | None = None,
        authorization: str | None = Header(default=None),
        settings: Settings = Depends(get_settings),
        store: FixtureStore = Depends(get_store),
    ):
        require_api_version(settings, api_version)
        check_auth(settings, authorization)

        p = store.project_by_id(organization, project_id)
        if not p:
            raise HTTPException(status_code=404, detail=f"Project not found: {project_id}")
        return JSONResponse(p)

    @app.get("/{organization}/{project}/_apis/git/repositories")
    def list_repositories(
        organization: str,
        project: str,
        api_version: str | None = None,
        top: int | None = None,
        skip: int | None = None,
        authorization: str | None = Header(default=None),
        settings: Settings = Depends(get_settings),
        store: FixtureStore = Depends(get_store),
    ):
        require_api_version(settings, api_version)
        check_auth(settings, authorization)

        repos = store.repos(organization, project)
        if repos == [] and not store.project_by_name(organization, project):
            raise HTTPException(status_code=404, detail=f"Project not found: {project}")

        repos = _apply_top_skip(repos, top=top, skip=skip)
        return JSONResponse(ado_envelope(repos))

    @app.get("/{organization}/{project}/_apis/git/repositories/{repo_id}")
    def get_repository(
        organization: str,
        project: str,
        repo_id: str,
        api_version: str | None = None,
        authorization: str | None = Header(default=None),
        settings: Settings = Depends(get_settings),
        store: FixtureStore = Depends(get_store),
    ):
        require_api_version(settings, api_version)
        check_auth(settings, authorization)

        repo = store.repo_by_id(organization, project, repo_id)
        if not repo:
            raise HTTPException(status_code=404, detail=f"Repository not found: {repo_id}")
        return JSONResponse(repo)

    @app.get("/{organization}/{project}/_apis/git/repositories/{repo_id}/refs")
    def list_refs(
        organization: str,
        project: str,
        repo_id: str,
        api_version: str | None = None,
        filter: str | None = None,  # noqa: A002 (match ADO param name)
        top: int | None = None,
        skip: int | None = None,
        authorization: str | None = Header(default=None),
        settings: Settings = Depends(get_settings),
        store: FixtureStore = Depends(get_store),
    ):
        require_api_version(settings, api_version)
        check_auth(settings, authorization)

        repo = store.repo_by_id(organization, project, repo_id)
        if not repo:
            raise HTTPException(status_code=404, detail=f"Repository not found: {repo_id}")

        refs = list(repo.get("refs", []))
        if filter:
            refs = [r for r in refs if str(r.get("name", "")).startswith(filter)]

        refs = _apply_top_skip(refs, top=top, skip=skip)
        return JSONResponse(ado_envelope(refs))

    return app
