from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class FixtureStore:
    data: dict[str, Any]

    @classmethod
    def load(cls, fixtures_path: str) -> "FixtureStore":
        p = Path(fixtures_path)
        if not p.exists():
            raise FileNotFoundError(f"Fixtures file not found: {p}")
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Fixtures root must be an object")
        return cls(data=data)

    def organization(self, org: str) -> dict[str, Any] | None:
        return (self.data.get("organizations") or {}).get(org)

    def project_by_id(self, org: str, project_id: str) -> dict[str, Any] | None:
        o = self.organization(org)
        if not o:
            return None
        for p in o.get("projects", []):
            if str(p.get("id")) == project_id:
                return p
        return None

    def project_by_name(self, org: str, project_name: str) -> dict[str, Any] | None:
        o = self.organization(org)
        if not o:
            return None
        for p in o.get("projects", []):
            if str(p.get("name")) == project_name:
                return p
        return None

    def repos(self, org: str, project_name: str) -> list[dict[str, Any]]:
        p = self.project_by_name(org, project_name)
        if not p:
            return []
        return list(p.get("repos", []))

    def repo_by_id(self, org: str, project_name: str, repo_id: str) -> dict[str, Any] | None:
        for r in self.repos(org, project_name):
            if str(r.get("id")) == repo_id:
                return r
        return None
