# GitHub Actions workflows

This directory contains the GitHub Actions workflows (pipelines) used by this repository.

## ci.yml

Continuous integration checks.

- Triggers: push, pull_request
- What it does:
  - Markdown lint (markdownlint-cli2)
  - Python tests (pytest)

## release-please.yml

Automated releases via Release Please.

- Triggers: push to main
- What it does:
  - Opens/updates a release PR and (when merged) creates GitHub Releases/tags based on conventional commits.

Note: commit/PR titles should follow **Conventional Commits** (typically `feat:` / `fix:` in lowercase). If changes are merged with non-matching titles (e.g. `Feat:`), Release Please may decide there is nothing to release.

## renovate.yml

Automated dependency update PRs via Renovate.

- Triggers:
  - Scheduled: Tuesday 04:00 UTC
  - Manual: workflow_dispatch
- Config: renovate.json
- Auth: uses the built-in GITHUB_TOKEN (no custom secret required)
