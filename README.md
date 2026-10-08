# Crypto Hardware Accel AESNI Agent

### [Open the Live Application →](https://abusuraihsakhri.github.io/crypto-hardware-accel-aesni-agent/)

A Python rule-based telemetry evaluator, with a lightweight browser interface, CLI, and FastAPI service. The browser application runs locally without a backend.

**Important limitation:** Despite the repository name, the current implementation does **not** execute AES-NI or ARMv8 cryptographic instructions, benchmark cryptographic throughput, detect hardware acceleration, test side-channel resistance, or establish compliance with NIST standards. Its thresholds are repository-defined heuristics, not cryptographic standard limits. Do not use the results as a security certification.

## Browser application

Open the [live interface](https://abusuraihsakhri.github.io/crypto-hardware-accel-aesni-agent/), enter task/target identifiers and numerical telemetry, then select **Evaluate locally**. Inspect the JSON result or use **Export JSON**. No server, account, or Python runtime is required.

The browser evaluator mirrors the three threshold/descriptor rules implemented in `agents/workers.py`:

- Primary metric > 25: elevated-risk alert.
- Secondary metric > 12: elevated-risk alert; an explicitly selected critical flag creates a critical alert.
- Status descriptor containing `DISCORDANT`, `ANOMALY`, `MUTANT`, `VIOLATION`, `FAIL`, or `REJECT` (case-insensitive): elevated-risk alert.

These are **illustrative inputs and rules**, not clinical or cryptographic acceptance criteria. An absence of alerts is not proof of integrity or security. The browser does not generate an HMAC audit trail.

## Python CLI

Python 3.9 or later is required. Install from a checkout:

```bash
python -m pip install -e ".[server,test]"
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --status ANOMALY
python cli.py batch -i sample.csv -o results.csv
python cli.py verify-audit
```

Run the API locally:

```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

Endpoints: `GET /health`, `GET /metrics`, `POST /api/audit`, `POST /api/chat`, and `GET /api/audit/logs`. The API has **no built-in authentication**; keep it bound to a trusted interface or add authentication and transport security before any public deployment.

The repository includes a separate compatibility implementation under `crypto_accel_aesni/`, with its own CLI and different thresholds. The published browser UI mirrors `agents/workers.py`, **not** the compatibility implementation.

## Data handling and security

- The browser sends no API requests and uses no analytics or persistent browser storage. Assessment results stay in the current tab until exported.
- The Python server stores dossiers and its HMAC-chained event records in **process memory**; restarting the process clears them. A persistent `AUDIT_SECRET_KEY` makes signatures reproducible with the same key, but does not persist the event records.
- The HMAC integrity check recomputes signatures and verifies chaining; it detects changes to retained record fields, but is **not** an independently anchored or durable audit ledger.
- Basic regular-expression checks reject several recognizable personal-identifier patterns. They do not constitute comprehensive de-identification or guarantee PHI/PII detection. Do not submit patient information, secrets, or production cryptographic key material.

For Docker Compose, set a strong secret first:

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
```

The `.env.example` file documents the variable; keep the real `.env` outside version control.

## Development and tests

```bash
python -m pip install -e ".[server,test]"
python -m pytest -q
node --check web/app.mjs
node --check web/evaluator.mjs
node --test tests/test_web.mjs
```

GitHub Actions tests Python 3.10–3.12 and the browser evaluator. A separate workflow deploys the static `web/` directory to GitHub Pages on updates to its contents.

**Technology:** Python, Pydantic 2, optional FastAPI/Uvicorn, vanilla HTML/CSS/JavaScript (ES modules). The web app targets current evergreen desktop and mobile browsers; it has no server-side Python or Pyodide dependency.

## License

[MIT](LICENSE).
