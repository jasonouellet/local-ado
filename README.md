# azure-api-mock

Service web qui mock un sous-ensemble de l’API REST **Azure DevOps**.

Objectif : permettre aux outils (Terraform, Ansible, scripts CI, apps) de parler à une URL “Azure DevOps-like” en local, avec des réponses déterministes.

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

Variables clés (préfixe `ADO_MOCK_`) :

- `FIXTURES_PATH` (défaut: `fixtures/demo.json`)
- `AUTH_MODE` : `none` | `pat` | `bearer`
- `TOKEN` : token attendu si auth activée
- `STRICT_API_VERSION` (bool)
- `ALLOWED_API_VERSIONS` (csv)
- `ARTIFICIAL_LATENCY_MS`

## Usage

- Avec docker compose : démarre sur `http://localhost:8080`
- Dataset par défaut : `demo-org` / `demo-project` / `demo-repo`

### Exemple (Ansible)

Utilise `ansible.builtin.uri` pour valider que le mock répond :

- URL: `http://localhost:8080/demo-org/_apis/projects?api-version=7.0`

### Exemple (Terraform)

Si tu veux simplement consommer une réponse JSON, tu peux utiliser le data source `http`.

⚠️ Pour le provider `microsoft/azuredevops`, tu peux tenter de pointer `org_service_url` vers le mock (ex: `http://localhost:8080/demo-org`), mais ça ne fonctionnera que si les endpoints nécessaires au provider sont implémentés.

## Notes

- Les réponses de liste utilisent l’enveloppe ADO : `{ "count": n, "value": [...] }`
- Les fixtures sont versionnées et déterministes.
