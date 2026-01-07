# Roadmap

This file tracks planned work and medium-term direction.
It is intentionally high-level and may change as real client needs evolve.

## Guiding principles

- **Client compatibility over perfection**: implement what real IaC/SDK clients call first.
- **Determinism**: stable IDs and fixtures whenever possible.
- **Minimal but sufficient payloads**: only include fields consumed by clients.

## Near-term focus

### Git Repos API (realism + surface area)

Goals:

- Add endpoints and behaviors needed by real clients.
- Improve realism without sacrificing determinism.

Examples of potential additions (as required by clients):

- More refs/branches behaviors (filtering, pagination, default branch semantics)
- Commits / changes / items APIs (only if used)
- Pagination improvements (continuation tokens if required)

### Pipelines API (minimal usable set)

Goals:

- Minimal endpoints to create/list/run pipelines.
- A simple simulation model for “runs” stored in-memory/fixtures.

Potential slices:

- List pipelines
- Get pipeline details
- Queue/run a pipeline
- List/get runs and status transitions

## Medium-term

### Record / replay mode (accelerator)

Add an optional mode to capture real Azure DevOps responses (without storing secrets) and replay them locally, to grow coverage faster.

### Optional stateful mode

Add optional persistence (e.g. SQLite) for POST/PATCH flows to enable more realistic scenarios while keeping the default deterministic fixture mode.

## Quality and tooling

### Tests

- Increase integration tests per endpoint
- Add contract tests (snapshots or schema) where helpful
- Add “client compatibility” scenario tests (Terraform/SDK flows)

### CI / security

- Lint (ruff) and tests in CI
- Optional future: dependency scanning and code scanning

## How to propose roadmap items

- Open an issue using the Feature Request template.
- Describe the target client (Terraform/SDK/CLI) and the required endpoints/fields.
- If possible, include HTTP traces (sanitized) to show what is actually needed.
