from __future__ import annotations

import base64
from typing import NamedTuple


class AuthResult(NamedTuple):
    ok: bool
    status_code: int
    message: str


def parse_basic_token(auth_header: str) -> str | None:
    """Parse PAT style Basic auth.

    Azure DevOps commonly uses: Authorization: Basic base64(":<PAT>")
    Some clients send username:<PAT>. We accept both.
    """

    if not auth_header.lower().startswith("basic "):
        return None

    b64 = auth_header.split(" ", 1)[1].strip()
    try:
        raw = base64.b64decode(b64).decode("utf-8", errors="replace")
    except Exception:
        return None

    # raw is "user:token" or ":token"
    if ":" not in raw:
        return None
    _user, token = raw.split(":", 1)
    token = token.strip()
    return token or None


def parse_bearer_token(auth_header: str) -> str | None:
    if not auth_header.lower().startswith("bearer "):
        return None
    token = auth_header.split(" ", 1)[1].strip()
    return token or None
