# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- (placeholder) Next LocalStack-like features (Terraform compatibility, pipelines, etc.).

## [0.1.0] - 2026-01-06

### Added
- Initial MVP: FastAPI service with Azure DevOps-like endpoints (projects + git repositories + refs).
- Fixture-driven deterministic dataset (`fixtures/demo.json`).
- Simulated auth modes (none/pat/bearer), api-version validation, basic pagination.
- Dockerfile/docker-compose, pytest suite, GitHub Actions CI.
