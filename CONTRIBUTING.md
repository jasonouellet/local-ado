# Contributing to azure-api-mock (local-ado)

Thanks for taking the time to contribute! This repository provides an **Azure DevOps-like** mock (Python/FastAPI) intended for local use with **deterministic** responses.

## Code of Conduct

By participating, you agree to follow our [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Project principles (read this first)

- **Client compatibility over perfection**: implement what real clients call first (Terraform/SDK/CLI).
- **Minimal-but-sufficient payloads**: include only the fields clients consume.
- **ADO conventions**: list envelopes like `{ "count": n, "value": [...] }`, expected HTTP codes, consistent JSON errors.
- **Determinism**: stable IDs and versioned fixtures whenever possible.

## Getting started (development)

Recommended: Python 3.12.

- Install dev dependencies:
  - `pip install -e '.[dev]'`
- Run tests:
  - `pytest -q`
- Run the server:
  - `python -m azure_api_mock`

The service listens on port 8080 by default (see `README.md`).

### Dev Container (optional)

A devcontainer is provided in `.devcontainer/`. In VS Code: **Reopen in Container**.

## Lint / format

- We use `ruff` (configured in `pyproject.toml`).
- Avoid drive-by formatting changes; keep diffs focused.

## Pre-commit (required)

This repository uses **pre-commit** to enforce formatting and linting consistency.

Before opening a PR, ensure pre-commit checks pass locally:

- Install hooks (once): `pre-commit install`
- Run on all files: `pre-commit run --all-files`

PRs are expected to keep pre-commit checks green (CI may run the same validations).

## Git workflow

We follow a “feature slice” approach:

- **One branch per feature** from `main`:
  - `feature/<area>-<topic>` (example: `feature/git-refs-pagination`)
- **One commit per step** (small, testable) using **Conventional Commits**.
  - Examples:
    - `feat(git): add refs filtering`
    - `fix(auth): return 401 for missing token`
    - `test: add integration test for repos list`
    - `docs: document new endpoints`

Tip: prefer the standard **lowercase** prefixes (`feat:`, `fix:`, etc.). This helps automation like Release Please detect changes consistently.

## What to contribute

Current priorities:

1. **Git Repos**: expand API surface and improve realism.
2. **Pipelines**: minimal endpoints to create/list/run pipelines.

For upcoming and medium-term work, see [`ROADMAP.md`](ROADMAP.md).

## Adding an endpoint (guide)

1. Identify the target client (Terraform/SDK) and the fields it reads/writes.
2. Add/adjust **integration tests** in `tests/`.
3. Implement the endpoint in `src/azure_api_mock/app.py` and/or state logic in `src/azure_api_mock/store.py`.
4. Ensure:
   - the response follows ADO conventions where applicable,
   - HTTP error codes are consistent (404/409/400…),
   - auth simulation and `api-version` behavior don’t regress.

## Security

If you believe you found a security issue, follow [`SECURITY.md`](SECURITY.md) (please don’t open a public issue).

## License

By contributing, you agree that your contributions will be licensed under this repository’s license (see `LICENSE`).
