from __future__ import annotations

import uvicorn

from .app import create_app
from .settings import Settings


def main() -> None:
    settings = Settings()
    uvicorn.run(create_app(), host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
