
# Instructions Copilot — Plan pour un service web de mock Azure DevOps

## Objectif
Tu dois produire **un plan d’implémentation actionnable** pour créer un service web qui **émule (mock)** un sous-ensemble de l’API REST **Azure DevOps** afin de permettre des tests/démos/développement local **sans dépendre d’Azure DevOps**.

Le résultat attendu est un plan structuré, avec des décisions explicites, des livrables, et des critères d’acceptation.

## Portée et principes
- Le mock doit viser la **compatibilité côté client** : mêmes routes, mêmes paramètres, mêmes codes de retour, et des payloads proches de l’API ADO.
- Le mock doit être **reproductible** : données déterministes via fixtures.
- Le mock doit être **facile à lancer** : une commande (ou docker compose) et une URL.
- Le mock doit être **observable** : logs, requêtes reçues, réponses renvoyées.

## Sorties (deliverables) à produire dans le plan
Le plan doit inclure au minimum :
1. **Périmètre d’API** (liste des endpoints à supporter en V1) + ce qui est explicitement hors scope.
2. **Architecture** (composants, modules, stockage des fixtures, routing, couche “comportement”).
3. **Modèle de données** (structure des fixtures, identifiants, relations).
4. **Authentification/autorisation** (simulée) et stratégie de validation des headers.
5. **Gestion d’erreurs** (codes, messages, cas limites).
6. **Stratégie de tests** (unit, intégration, contract tests) et automatisation CI.
7. **Configuration** (ports, baseUrl, mode strict/lenient, latence simulée).
8. **Plan de livraison** (jalons, tâches, définition du “done”).

## Étapes recommandées (structure du plan)
### 1) Définir les cas d’usage
- Qui consomme le mock (CLI, app, tests E2E, pipelines, etc.) ?
- Quelles opérations doivent fonctionner : lecture (GET), création (POST), mise à jour (PATCH/PUT), suppression (DELETE) ?
- Contraintes : offline, latence simulée, datasets multiples, multi-tenant (org/projet).

### 2) Choisir la stratégie de mock
Le plan doit choisir l’une (ou un mix) :
- **Mock par contrats** : réponses basées sur OpenAPI/JSON Schema (si disponible) + validation.
- **Mock par enregistrements** : replay de réponses capturées (cassette/VCR HTTP) avec paramétrage.
- **Mock par comportement** : logique métier minimale (création d’ID, pagination, filtrage, transitions d’état).

### 3) Lister les endpoints ADO à supporter (V1)
Le plan doit proposer une liste initiale réaliste, par exemple (à adapter aux besoins) :
- **Projects** :
	- GET `/{organization}/_apis/projects?api-version=...`
	- GET `/{organization}/_apis/projects/{projectId}?api-version=...`
- **Git** :
	- GET `/{organization}/{project}/_apis/git/repositories?api-version=...`
	- GET `/{organization}/{project}/_apis/git/repositories/{repoId}?api-version=...`
	- GET `/{organization}/{project}/_apis/git/repositories/{repoId}/refs?filter=...&api-version=...`
- **Build / Pipelines** (selon besoin) :
	- GET `/{organization}/{project}/_apis/build/definitions?api-version=...`
	- GET `/{organization}/{project}/_apis/build/builds?definitions=...&statusFilter=...&api-version=...`
	- (ou Pipelines) GET `/{organization}/{project}/_apis/pipelines?api-version=...`
- **Work Items (WIT)** (si requis) :
	- POST `/{organization}/{project}/_apis/wit/wiql?api-version=...`
	- GET `/{organization}/_apis/wit/workitems?ids=...&fields=...&api-version=...`

Pour chaque endpoint du plan, préciser :
- paramètres supportés (query/path)
- structure de réponse (minimalement les champs utilisés par le client)
- codes HTTP possibles (200/201/400/401/403/404/409/429/500)
- pagination (continuation token, top/skip)

### 4) Compatibilité des détails “Azure DevOps-like”
Inclure explicitement dans le plan :
- support de `api-version` (accepté/validé, éventuellement mode strict)
- headers importants (ex: `Authorization`, `Accept`, `Content-Type`)
- enveloppes ADO fréquentes : `{ "count": n, "value": [...] }`
- erreurs au format JSON (et éventuellement `VssServiceResponse`-like si utile)

### 5) Données : fixtures et état
Le plan doit décider si le mock est :
- **Stateless** (fixtures en lecture seule)
- **Stateful** (créations/modifs en mémoire ou DB légère)

Recommandation par défaut :
- fixtures versionnées dans le repo (`fixtures/`), + option d’override par variable d’env
- mode stateful via **SQLite** ou stockage fichier JSON, pour permettre POST/PATCH pendant les tests

Définir :
- format des fixtures (JSON/YAML)
- conventions d’IDs (GUID-like), noms, URLs
- datasets (ex: `small`, `demo`, `edge-cases`)

### 6) Architecture du service
Le plan doit proposer une structure modulaire, par exemple :
- `src/server` : bootstrap HTTP, middlewares
- `src/routes` : mapping routes ADO → handlers
- `src/handlers` : logique par domaine (projects/git/build/wit)
- `src/store` : lecture/écriture fixtures, state management
- `src/validation` : validation query/headers/schemas
- `src/errors` : génération d’erreurs cohérentes

Inclure :
- logs structurés (JSON) + correlation id (header type `x-correlation-id`)
- option de latence simulée et de “fault injection” (timeouts, 500, 429)

### 7) Sécurité (mock)
Le plan doit préciser :
- acceptation d’un PAT fictif (ex: Basic base64 `:{token}`) ou Bearer
- règles simples : token manquant → 401, token invalide → 403
- mode “no-auth” pour local si souhaité

Ne jamais demander ni stocker de secrets réels.

### 8) Tests et qualité
Inclure :
- tests d’intégration par endpoint (supertest/pytest/httpx)
- tests de contrats : snapshots de réponse, ou JSON schema validation
- scénarios edge-cases : pagination vide, 404, 409 (duplicate), 429 rate limit
- lint/format + CI

### 9) Expérience développeur
Le plan doit prévoir :
- documentation de lancement (README), exemples curl, exemples de config client
- healthcheck : `GET /healthz`
- endpoint optionnel d’inspection : `GET /__admin/routes`, `GET /__admin/fixtures`

## Format attendu du plan
Rends le plan en sections claires, avec :
- une **liste de jalons** (MVP → v1 → v2)
- une **table** “Endpoint → statut → notes”
- des **critères d’acceptation** mesurables (ex: “tel client passe ses tests”, “tel endpoint supporte top/skip”, etc.)

## Définition du MVP (recommandation)
Le MVP doit au minimum :
- démarrer un serveur HTTP
- exposer 2–4 endpoints critiques (ex: projects + repos)
- charger des fixtures
- gérer `api-version` + auth simple
- fournir des réponses conformes au client (payload minimal)

