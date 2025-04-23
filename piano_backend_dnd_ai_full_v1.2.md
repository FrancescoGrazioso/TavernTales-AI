# Piano di Progetto Backend – TavernTales-AI
*Versione 1.2 – 19 Aprile 2025*

> Documento completo di **Epiche → Card → Task → Sub‑task** con descrizioni, criteri di accettazione (AC) e stime in story‑points (SP).

## Legend
- **AC** – Acceptance Criteria
- **EST** – Effort estimate in story‑points (1 SP ≈ 0.5 giorni dev)

### EPICA 1 – Gestione Utente & Autenticazione
#### Card 1.1 – Registrazione & Login

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **1.1.1** | Setup progetto<br>inizializzare repo, Django, DRF, SimpleJWT |       - crea repo Git + commit iniziale
      - configura virtualenv e Pipfile
      - boilerplate settings.py | Ambiente avviabile con `python manage.py runserver` | 3 |
| **1.1.2** | CustomUser model<br>creare modello e manager personalizzato |       - definisci fields e meta
      - scrivi migrazioni
      - registralo in admin | `createsuperuser` funziona e salva record | 2 |
| **1.1.3** | Endpoint auth<br>implementare signup/login/token |       - serializzatori DRF
      - views APIView
      - tests Postman collection | Ricevo e posso rinnovare JWT | 3 |
| **1.1.4** | Test unit e integrazione<br>coprire modelli e API |       - setup pytest
      - writing tests
      - coverage badge | Pipeline GitHub Actions verde, coverage ≥90 % | 2 |

#### Card 1.2 – Recupero password & Profilo

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **1.2.1** | Forgot‑password flow<br>invio link reset e cambio password |       - generatore token
      - template email SendGrid
      - endpoint reset | Password può essere reimpostata via link email | 3 |
| **1.2.2** | API profilo<br>endpoint per aggiornare dati utente |       - serializer profilo
      - upload avatar S3
      - patch username/email | Chiamata PATCH aggiorna e restituisce dati | 2 |

### EPICA 2 – Gestione Personaggio
#### Card 2.1 – Modello Character

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **2.1.1** | Definizione modello<br>modellare campi D&D completi |       - campi abilità, risorse
      - relazioni inventory, spells
      - migrazione e admin | Migrazioni applicate senza errori | 5 |
| **2.1.2** | CRUD API<br>endpoints list/retrieve/update/delete |       - serializers
      - viewsets
      - routers | Operazioni CRUD testate via Postman | 3 |
| **2.1.3** | Validazioni business<br>limiti livelli, punti caratteristica |       - validatori clean
      - test edge cases | Input invalido genera 400 dettagliato | 2 |

#### Card 2.2 – Import / Export scheda

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **2.2.1** | Import JSON<br>caricare file JSON ufficiale e creare Personaggio |       - schema json
      - parser
      - unit test | File valido produce Character popolato | 3 |
| **2.2.2** | Export PDF<br>generare PDF scheda via WeasyPrint |       - template HTML
      - stili CSS compatibles
      - endpoint download | PDF riflette dati DB e si scarica | 3 |

### EPICA 3 – Party, Sessioni & Messaggi
#### Card 3.1 – Party

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **3.1.1** | Modello Party<br>owner, invite, members |       - campo invite_code unico
      - view join party
      - tests | Utente può creare e altri unirsi con codice | 2 |

#### Card 3.2 – Session

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **3.2.1** | Modello Session<br>status lifecycle |       - campi timestamps
      - foreign key party
      - admin | Sessione creata via API | 2 |
| **3.2.2** | Lifecycle endpoints<br>start/pause/finish |       - permission check
      - state machine | Transizioni rispettano diagramma stati | 2 |

#### Card 3.3 – ChatMessage

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **3.3.1** | Definizione modello<br>contenuto, jsonb, indice FTS |       - content field
      - toxicity_score
      - GIN index | Ricerca full‑text ritorna risultati | 3 |
| **3.3.2** | API paginazione<br>cursor‑based list |       - pagination class
      - ordering desc | Frontend può effettuare infinite scroll | 2 |

### EPICA 4 – Integrazione AI (Gemini)
#### Card 4.1 – Client Wrapper

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **4.1.1** | Classe service Gemini<br>gestione chiavi, retry, metrics |       - implementa exponential backoff
      - prometheus counter | Success rate ≥99 % | 3 |

#### Card 4.2 – Gestione contesto

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **4.2.1** | Sliding window<br>limita ultimo N messaggi |       - config setting
      - unit tests | Finestra adattabile runtime | 2 |
| **4.2.2** | Summaries long‑term<br>riassunti salvati ogni M msg |       - algoritmo TL;DR
      - persistenza summary | Context < 8k token | 3 |
| **4.2.3** | Persistenza history<br>riavvio server recovery |       - ai_context_id mapping
      - db lookup | Conversazione continua dopo restart | 2 |

#### Card 4.3 – Parsing risposta AI

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **4.3.1** | Schema JSON output<br>definire pydantic model |       - fields narrative, updates
      - error handling | Output valido contro schema | 2 |
| **4.3.2** | Update Character<br>applica modifiche stats |       - atomic transaction
      - audit log | Character riflette effetti AI | 3 |

### EPICA 5 – Motore Regole & Dadi
#### Card 5.1 – Dice Roller

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **5.1.1** | Parser formula<br>supporto XdY+Z |       - regex tokenize
      - random generator | Risultato corretto rispetto a seed | 2 |
| **5.1.2** | Edge cases<br>advantage/disadvantage |       - roll 2d20 pick high/low
      - unit tests property | Funzioni passano test proprietà | 2 |

#### Card 5.2 – Validatore SRD

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **5.2.1** | Regole base<br>HP non negativi, incantesimi slot |       - lookup tables
      - exceptions | Violazione produce error code | 3 |
| **5.2.2** | Hook pre‑AI<br>intercetta azioni illegali |       - middleware session
      - unit tests | Azioni illegali vengono rigettate | 2 |

### EPICA 6 – Sincronizzazione Stato Personaggio
#### Card 6.1 – Job aggiornamento

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **6.1.1** | Mapper AI→DB<br>traduci updates in mutate |       - field map config
      - edge cases | Tutti cambiamenti salvati | 2 |
| **6.1.2** | Transazioni atomiche<br>blocco pessimista |       - select FOR UPDATE
      - retry logic | No race condition HP | 2 |
| **6.1.3** | WebSocket notify<br>broadcast patch |       - channels group_send
      - payload diff | Client riceve update <100ms | 1 |

### EPICA 7 – API REST & WebSocket
#### Card 7.1 – Versioned REST

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **7.1.1** | OpenAPI schema<br>drf-spectacular |       - swagger UI
      - redoc | Spec pubblicata /docs | 1 |
| **7.1.2** | Rate limiting<br>throttling classes |       - anon vs auth
      - redis cache | 429 su abuso | 1 |

#### Card 7.2 – Realtime Channels

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **7.2.1** | Setup Redis broker<br>docker-compose |       - settings channel_layer
      - healthcheck | WS connection successful | 1 |
| **7.2.2** | Chat namespace<br>/ws/session/{id} |       - consumer class
      - auth middleware | Messaggi broadcast a iscritti | 2 |
| **7.2.3** | Events update<br>chat.message, state.patch |       - serializer event
      - tests | Frontend riceve eventi previsti | 2 |

### EPICA 8 – DevOps & Deployment
#### Card 8.1 – Containerization

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **8.1.1** | Dockerfile multi‑stage<br>build, slim runtime |       - python:3.12
      - poetry export | Image <200 MB | 2 |
| **8.1.2** | docker‑compose<br>services db, redis, app |       - env vars
      - volumes | `docker compose up` funziona | 1 |

#### Card 8.2 – CI/CD

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **8.2.1** | GitHub Actions<br>lint, test, build |       - matrix python
      - coverage upload | Workflow completato | 2 |
| **8.2.2** | Deploy Fly.io<br>blue‑green |       - fly.toml
      - release command migrate | Deploy automatico main branch | 2 |

#### Card 8.3 – Observability

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **8.3.1** | Logging JSON<br>structlog + Loki |       - correlation id
      - filters | Logs visibili in Grafana | 1 |
| **8.3.2** | Metrics Prometheus<br>django-prometheus |       - exporter
      - dashboards | Grafico latency API | 1 |

### EPICA 9 – Testing & Quality Assurance
#### Card 9.1 – Unit Coverage

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **9.1.1** | Pytest<br>fixtures factory boy |       - param tests
      - tox envs | Coverage ≥80 % | 2 |

#### Card 9.2 – Integration AI

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **9.2.1** | Mock Gemini<br>httpretty stub |       - fixture sample
      - latency | Tests offline pass | 2 |
| **9.2.2** | Contract tests<br>response schema |       - jsonschema file
      - CI stage | Unexpected fields fail test | 1 |

#### Card 9.3 – Load testing

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **9.3.1** | Locust plan<br>10k ws users |       - spike scenario
      - charts | 95th < 500ms | 3 |

### EPICA 10 – Sicurezza, Moderazione & Compliance
#### Card 10.1 – Content Moderation

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **10.1.1** | Moderation API<br>OpenAI/Perspective |       - async check
      - score threshold | Toxicity < limit flagged | 2 |
| **10.1.2** | Lockdown logic<br>session freeze |       - max violations
      - notification | Sessione bloccata su abusi | 2 |

#### Card 10.2 – GDPR & Data Security

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **10.2.1** | Data retention<br>cron delete logs |       - configurable days
      - legal review | Cron cancella record > limit | 1 |
| **10.2.2** | Encryption at rest<br>PostgreSQL TLS, secrets |       - sslmode
      - doppler secrets | SSL enforced | 1 |

#### Card 10.3 – Rate‑limiting

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **10.3.1** | Token bucket<br>Redis Lua |       - per‑user windows
      - test flood | 429 after limit | 1 |

### EPICA 11 – Documentazione & Onboarding
#### Card 11.1 – Dev Handbook

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **11.1.1** | README<br>setup, make commands |       - local env
      - scripts | New dev runs app in 10m | 1 |
| **11.1.2** | ADR repo<br>decisions markdown |       - template
      - sample | ADR rendered on GitHub | 1 |

#### Card 11.2 – API Reference

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **11.2.1** | Swagger UI<br>container route |       - redoc page
      - example curl | Docs public at /docs | 1 |
| **11.2.2** | Code snippets<br>python/js examples |       - gist embed
      - CI publish | Snippets tested | 1 |

### EPICA 12 – Administration & RBAC
#### Card 12.1 – Roles & Permissions

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **12.1.1** | Define roles<br>admin, mod, player, guest |       - enum choices
      - seed data | Role assigned on signup | 1 |
| **12.1.2** | Policy decorators<br>DRF permission classes |       - tests access
      - 403 forbidden | Endpoints enforce policy | 2 |

#### Card 12.2 – Admin Dashboard

| Task ID | Titolo / Descrizione | Sub‑task | AC | EST |
|---------|---------------------|----------|----|-----|
| **12.2.1** | Branding<br>logo, theme |       - base template
      - dark mode | Admin logo replaced | 1 |
| **12.2.2** | Stats panel<br>active sessions, cost |       - query ai_request_log
      - chart.js | Numbers update live | 2 |

## Roadmap Sprint
| Sprint | Obiettivo principale | Epiche coperte |
|--------|----------------------|----------------|
| 0 | Setup repo, CI baseline | 1 |
| 1‑2 | Auth & Character CRUD | 1,2 |
| 3‑4 | Party/Session & WS POC | 3,7 |
| 5‑6 | AI integration MVP | 4,5,6 |
| 7 | Security & Moderation | 10 |
| 8 | DevOps hardening | 8 |
| 9 | Load & QA | 9 |
| 10 | RBAC & Admin | 12 |
| 11 | Beta Release | All |