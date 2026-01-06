 
# Instructions Copilot — local-ado (Azure DevOps LocalStack-like)

## Contexte (ce qui existe déjà)
Ce repo contient déjà un **MVP fonctionnel** d’un mock Azure DevOps en **Python/FastAPI**.

### Fonctionnalités déjà implémentées
- Serveur FastAPI (`src/azure_api_mock/app.py`) + exécution `python -m azure_api_mock`.
- Config par variables d’environnement (préfixe `ADO_MOCK_`) : `settings.py`.
- Fixtures déterministes (`fixtures/demo.json`) chargées via `store.py`.
- Auth simulée : `none` / `pat` (Basic) / `bearer`.
- `api-version` (validation optionnelle) + pagination simple `top/skip`.
- Observabilité minimale : logs JSON + `x-correlation-id`.
- Admin : `GET /__admin/routes`, `GET /__admin/fixtures`.
- Dockerfile + docker-compose + tests pytest + CI GitHub Actions.

### Endpoints (MVP)
- `GET /{org}/_apis/projects?api-version=...`
- `GET /{org}/_apis/projects/{projectId}?api-version=...`
- `GET /{org}/{project}/_apis/git/repositories?api-version=...`
- `GET /{org}/{project}/_apis/git/repositories/{repoId}?api-version=...`
- `GET /{org}/{project}/_apis/git/repositories/{repoId}/refs?filter=...&api-version=...`

## Cible (vision)
Construire un équivalent **LocalStack-like** pour Azure DevOps : un service local “Azure DevOps-like” utilisable par :
- Terraform / Ansible / scripts CI (IaC-first)
- SDKs et outils (curl/http clients)

La priorité fonctionnelle immédiate :
1) **Repos** (Git) : enrichir la surface API et le comportement
2) **Pipelines** (Azure Pipelines) : endpoints nécessaires pour créer/consulter/exécuter des pipelines
Le reste (boards/WIT, service connections, variable groups, permissions) est planifié pour des itérations suivantes.

### Ressources Terraform ciblées (itération actuelle)
Le mock doit viser en premier la compatibilité avec ces ressources du provider Terraform `microsoft/azuredevops` :
- `azuredevops_project`
- `azuredevops_git_repository`
- `azuredevops_build_definition` (**moderne seulement**) : interpréter “moderne” comme **YAML pipeline** (pas de designer/classic UI), donc implémenter le strict minimum côté `/ _apis/build/definitions` utilisé pour les définitions YAML.

## Règles de contribution (important)
### Compatibilité client > perfection
- Implémenter d’abord **les endpoints réellement appelés** par les clients IaC/SDK.
- Garder les payloads **minimaux mais suffisants** (champs consommés).
- Respecter les conventions ADO : enveloppes `{ "count": n, "value": [...] }`, codes HTTP, erreurs JSON.

### Workflow Git obligatoire (branche par fonctionnalité, commit par étape)
Objectif : itérer vite sans perdre la traçabilité.

Règles :
- **Une branche par fonctionnalité** (ou “feature slice”), créée depuis `main`.
  - Convention de nom : `feature/<domaine>-<sujet>` (ex: `feature/project-crud`, `feature/build-def-yaml`).
- **Un commit par étape du todo** : chaque item du todo correspond à **au moins** 1 commit.
  - Si un item est gros, le découper en sous-items (et donc plusieurs commits) avant de coder.
- Chaque commit doit être :
  - **petit**, testable, et idéalement avec tests ajoutés/ajustés dans le même commit.
  - accompagné d’un message de commit clair suivant le style Conventional Commits.

Conventions de message (recommandées) :
- `feat(project): ...` / `feat(git): ...` / `feat(build): ...`
- `test: ...`
- `docs: ...`
- `ci: ...`
- `refactor: ...`
- `chore: ...`

Stratégie de merge :
- Ouvrir une PR par branche feature.
- Garder l’historique lisible (merge commit ou squash selon préférence, mais conserver la granularité si possible).

### Changelog et versions (obligatoire sur `main`)
Le repo doit maintenir un `CHANGELOG.md` **mis à jour pour chaque version publiée** sur la branche `main`.

Règles :
- Format : **Keep a Changelog** + **Semantic Versioning**.
- Toute modification notable doit être ajoutée dans `## [Unreleased]` via la PR correspondante.
- Au moment de publier une version (tag/release) :
  - déplacer les entrées de `Unreleased` dans une section `## [x.y.z] - YYYY-MM-DD`
  - conserver `Unreleased` vide (ou avec placeholders) pour la suite
  - mettre à jour la version du projet (ex: `pyproject.toml`) si applicable.

Idéalement, automatiser plus tard (ex: release tooling) mais **ne pas bloquer** l’itération fonctionnelle.

## Méthode d’itération (pour être plus performant)
Quand tu ajoutes une capacité (endpoint, ressource Terraform, pipeline), applique ce protocole :

1) **Définir la cible “client”**
  - Quelle ressource Terraform (ou tâche Ansible) doit fonctionner ?
  - Quels attributs le client lit/écrit ?

2) **Identifier la surface API minimale**
  - Lister les endpoints précis nécessaires (routes + query params + codes de retour).
  - Documenter les payloads minimaux (champs réellement consommés).

3) **Écrire/mettre à jour des tests d’intégration**
  - Ajouter un test “happy path” et 1–2 edge cases (404, 409, pagination, auth).
  - Les tests doivent reproduire un flux client (create → read → update → delete) quand applicable.

4) **Implémenter le comportement**
  - D’abord le chemin minimal (fixtures/store) puis le réalisme par itérations.
  - Favoriser le déterminisme (IDs stables si possible).

5) **Contract tests (quand ça devient utile)**
  - Ajouter des snapshots ou JSON schema pour stabiliser les réponses.

6) **Boucle rapide**
  - Après chaque étape/commit : exécuter tests + lint (localement et via CI).

### “IaC-first” (méthode de livraison)
Pour chaque itération :
1. Choisir **3–5 ressources IaC** cibles (Terraform provider `microsoft/azuredevops` et/ou tâches Ansible).
2. Identifier les endpoints requis (par traces HTTP / docs / inspection du provider).
3. Implémenter endpoints + pagination/filtrage + erreurs.
4. Ajouter tests d’intégration + tests de contrat (snapshots ou JSON schema).

## Prochaines capacités LocalStack-like (roadmap)
Copilot doit aider à implémenter, dans cet ordre (ajuste si nécessaire) :

### Itération A — Git (repos) “plus réaliste”
- Ajouter support de nouveaux endpoints Git (exemples)
  - branches/refs avancées, commits (si nécessaires), items (si nécessaires)
- Ajouter pagination ADO plus réaliste (continuation token si requis par les clients)

### Itération B — Pipelines
- Supporter une API pipelines “utilisable” localement :
  - listing pipelines, détails pipeline, runs/executions, status
- Prévoir un moteur de simulation (runs stockés, transitions d’état).

### Itération C — Record/Replay (accélérateur)
- Ajouter un mode optionnel **record/replay** pour capturer des réponses ADO réelles (sans stocker de secrets).
- Objectif : enrichir rapidement fixtures + comportements sans tout coder à la main.

### Itération D — Mode stateful optionnel
- Ajouter persistence SQLite optionnelle pour POST/PATCH (scénarios plus réalistes).

## Qualité, CI, sécurité supply-chain (exigences)
### Tests
- Monter en niveau :
  - tests d’intégration par endpoint
  - tests “contract” (snapshots/schema)
  - tests de compatibilité “client” (scénarios IaC/SDK)

### CI complet
Le CI doit à terme inclure :
- tests + couverture
- analyse statique Python (ex: ruff, mypy)
- scans : Sonar (SonarCloud/SonarQube) + Snyk

### Renovate
- Ajouter une config Renovate pour suivi automatique des versions (Python deps + GitHub Actions + Docker).

### Conteneurs
- Les images d’exécution doivent être **light** : base slim, multi-stage si utile, pas d’outils dev dans l’image runtime.
- Fournir un healthcheck.

### Devcontainer
- Ajouter une configuration `.devcontainer/` portable (Python + deps + tâches) pour développement local reproductible.

## Documentation
Objectif : documentation **MkDocs** compatible (ex: `mkdocs.yml` + `docs/`).
Inclure :
- démarrage rapide (docker/compose)
- configuration (env)
- endpoints supportés + exemples curl
- guides “Terraform/Ansible” (et limitations connues)
- contribution (comment ajouter un endpoint)

