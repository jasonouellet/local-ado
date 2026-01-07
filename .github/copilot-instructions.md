# Copilot Instructions — local-ado (Azure DevOps LocalStack-like)

## Language for public-facing files (important)

All **public-facing repository files** must be written in **English**.

This includes (non-exhaustive):

- `README.md`, `CHANGELOG.md`
- `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`
- GitHub templates under `.github/` (issue templates, PR template)
- Documentation under `docs/` (when added)

## Where to look (canonical repo docs)

Avoid duplicating long policies or contribution details in this file. Use these files as the source of truth:

- `README.md`: usage, configuration, and currently supported endpoints.
- `CONTRIBUTING.md`: how to contribute (workflow, how to test, scope, priorities).
- `CODE_OF_CONDUCT.md`: community rules.
- `SECURITY.md`: how to report vulnerabilities (no public issues).
- `SUPPORT.md`: where/how to ask for help.
- `CHANGELOG.md`: notable changes and release notes.
- `ROADMAP.md`: upcoming work and medium-term direction.

## Codebase map (for implementation)

- `src/azure_api_mock/app.py`: FastAPI app and routes.
- `src/azure_api_mock/store.py`: fixture-backed state and lookup helpers.
- `src/azure_api_mock/settings.py`: configuration (env vars prefixed with `ADO_MOCK_`).
- `src/azure_api_mock/http_utils.py`: HTTP helpers (pagination, headers, etc.).
- `fixtures/demo.json`: deterministic demo dataset.
- `tests/`: pytest integration tests.

## Copilot engineering guidelines

- **Client compatibility over perfection**: implement the endpoints real IaC/SDK clients call first.
- **Minimal but sufficient payloads**: add only fields actually consumed by clients.
- **ADO conventions**: list envelopes `{ "count": n, "value": [...] }`, consistent HTTP codes, consistent JSON error shapes.
- **Determinism**: prefer stable IDs and deterministic fixtures.
- **Tests-first when possible**: add/adjust integration tests in `tests/` for each endpoint/behavior.

## Current focus (near term)

- Git Repos API realism and surface area.
- Pipelines API: minimal endpoints to create/list/run pipelines.
- Terraform provider compatibility targets (current iteration):
  - `azuredevops_project`
  - `azuredevops_git_repository`
  - `azuredevops_build_definition` (YAML/modern only)

For step-by-step contribution workflow, commit conventions, and changelog requirements, follow `CONTRIBUTING.md`.

For planned/upcoming items, see `ROADMAP.md`.
