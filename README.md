# azure-api-mock

Web service that mocks a subset of the **Azure DevOps** REST API.

Goal: allow tools (Terraform, Ansible, CI scripts, apps) to talk to an “Azure DevOps-like” URL locally, with deterministic responses.

Roadmap: [`ROADMAP.md`](ROADMAP.md)

Contributing: [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Endpoints (MVP)

- `GET /healthz`
- `GET /__admin/routes`
- `GET /__admin/fixtures`

Azure DevOps-like (MVP) :

- `GET /{organization}/_apis/projects?api-version=...`
- `GET /{organization}/_apis/projects/{projectId}?api-version=...`
- `GET /{organization}/{project}/_apis/git/repositories?api-version=...`
- `GET /{organization}/{project}/_apis/git/repositories/{repoId}?api-version=...`
- `GET /{organization}/{project}/_apis/git/repositories/{repoId}/refs?filter=...&api-version=...`

## Configuration (env)

Key variables (prefix `ADO_MOCK_`):

- `FIXTURES_PATH` (default: `fixtures/demo.json`)
- `AUTH_MODE`: `none` | `pat` | `bearer`
- `TOKEN`: expected token when auth is enabled
- `STRICT_API_VERSION` (bool)
- `ALLOWED_API_VERSIONS` (csv)
- `ARTIFICIAL_LATENCY_MS`

## Usage

- With docker compose: starts on `http://localhost:8080`
- Default dataset: `demo-org` / `demo-project` / `demo-repo`

### Example (Ansible)

Use `ansible.builtin.uri` to validate that the mock responds:

- URL: `http://localhost:8080/demo-org/_apis/projects?api-version=7.0`

### Example (Terraform)

If you simply want to consume a JSON response, you can use the `http` data source.

⚠️ For the `microsoft/azuredevops` provider, you can try pointing `org_service_url` to the mock (e.g. `http://localhost:8080/demo-org`), but it will only work for the endpoints that are implemented.

## Notes

- List responses use the ADO envelope: `{ "count": n, "value": [...] }`
- Fixtures are versioned and deterministic.
