# Backend Local Setup

This guide uses the real backend repository:

```text
https://github.com/adriankae/Eczema-Tracker
```

## 1. Clone the backend

```bash
git clone https://github.com/adriankae/Eczema-Tracker.git
cd Eczema-Tracker
```

## 2. Start Docker

The repository includes a `docker-compose.yml` with PostgreSQL and the API container.

```bash
docker compose up -d --build
```

Expected services:

- API on `http://localhost:8000`
- PostgreSQL on `localhost:5432`

## 3. Backend environment variables

The compose file uses these defaults:

- `DATABASE_URL=postgresql+psycopg://eczema:eczema@postgres:5432/eczema`
- `APP_ENV=local`
- `DEPLOYMENT_TIMEZONE=UTC`
- `ENABLE_SCHEDULER=true`
- `JWT_SECRET=change-me-in-production`
- `INITIAL_USERNAME=admin`
- `INITIAL_PASSWORD=admin`

Assumption used for the CLI docs:

- the backend is reachable at `http://localhost:8000`
- the deployment timezone is UTC unless you change the backend settings

## 4. Confirm the API is reachable

```bash
curl -sS http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## 5. Obtain an API key

Login with the seeded account:

```bash
curl -sS -X POST http://localhost:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"admin"}'
```

The response includes an `access_token`.

Create a programmatic API key:

```bash
curl -sS -X POST http://localhost:8000/api-keys \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"name":"czm-cli"}'
```

The response includes `plaintext_key`. That value is what `czm` stores as `api_key`.

## 6. Configure the CLI

Example config file:

```toml
base_url = "http://localhost:8000"
api_key = "paste-the-plaintext-key-here"
timezone = "Europe/Berlin"
```

## 7. Notes

- The backend seeds `admin` / `admin` on first startup if no account exists.
- The backend uses `X-API-Key` for API key authentication.
- `czm` does not need the bearer token after the API key is created.

