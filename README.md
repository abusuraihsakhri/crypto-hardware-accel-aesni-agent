# Crypto Hardware Accel Aesni Agent

> **Domain:** Post-Quantum Cryptography & Zero-Knowledge Architecture
> **Reference Guidelines & Standards:** `NIST FIPS 203/204/205, NIST SP 800-90B & ISO/IEC Standards`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

Crypto Hardware Accel Aesni Agent is an enterprise-grade distributed component platform for cryptographic hardware acceleration auditing and post-quantic cryptography compliance verification. It provides:

- Multi-agent consensus evaluation with specialized workers for QC, safety, and protocol conformance
- Tamper-evident HMAC-SHA256 audit trail for all operations
- Zero-PHI outbound guard to prevent sensitive data leakage
- FastAPI REST API with Prometheus telemetry metrics
- CLI interface for single evaluations, batch processing, and interactive chat

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization (ROUTINE, ELEVATED, CRITICAL_STAT) with automated action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking, identifier validation, and anomaly detection.
- **Multi-Agent Consensus**: Three specialized workers (InvariantQC, SafetyEscalation, ProtocolConformance) provide comprehensive evaluation.

---

## 💻 CLI Quickstart & Usage

### Installation

```bash
pip install -e .
```

### 1. Single Task Evaluation (Audit)
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Interactive Chat
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
- `--task-id`: Unique task identifier (alphanumeric, hyphens, underscores)
- `--target`: Target identifier (alphanumeric, hyphens, underscores)
- `--primary`: Primary metric value (float)
- `--secondary`: Secondary metric value (float)
- `--critical`: Flag for critical priority
- `--status`: Status descriptor (e.g., NOMINAL, DISCORDANT, ANOMALY)

### Input Data Schema (CSV Batch)

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Unique task identifier | Required |
| `target_identifier` | Target entity identifier | Required |
| `primary_metric` | Primary measurement value | Required |
| `secondary_metric` | Secondary measurement value | Optional |
| `is_critical_flag` | Critical priority flag | Optional |
| `status_descriptor` | Status code descriptor | Optional |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Input Validation:** Strict identifier validation with character and length constraints.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

### Security Configuration

Set the `AUDIT_SECRET_KEY` environment variable for persistent audit integrity:

```bash
# Linux/macOS
export AUDIT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Windows PowerShell
$env:AUDIT_SECRET_KEY = -join ((1..32) | ForEach-Object { '{0:x}' -f (Get-Random -Max 16) })
```

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py --tasks 1000 --concurrency 8
```

---

## 🐳 Container Deployment

```bash
docker build -t crypto-hardware-accel-aesni-agent .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secret-key crypto-hardware-accel-aesni-agent
```

Or using Docker Compose:

```bash
AUDIT_SECRET_KEY=your-secret-key docker-compose up -d
```

---

## 📁 Project Structure

```
crypto-hardware-accel-aesni-agent/
├── agents/                    # Core agent framework
│   ├── api.py                 # FastAPI REST server
│   ├── base.py                # Security, PHI guard, audit trail
│   ├── models.py              # Pydantic data models
│   ├── supervisor.py          # Main supervisor orchestrator
│   ├── workers.py             # Specialized evaluation workers
│   ├── llm_factory.py         # LLM provider factory
│   ├── learning.py            # Bayesian calibration engine
│   ├── metrics.py             # Prometheus metrics collector
│   └── streamer.py            # WebSocket telemetry streamer
├── crypto_accel_aesni/        # Secondary AES-NI auditor package
│   ├── agents.py              # Hardware crypto coordinator
│   ├── engine.py              # Core algorithmic engine
│   ├── models.py              # Data models
│   ├── server.py              # FastAPI server factory
│   └── cli.py                 # CLI interface
├── tests/                     # Test suite
├── cli.py                     # Main CLI entry point
├── simulator.py               # High-throughput simulator
├── enrichment.py              # Enrichment feature modules
├── pyproject.toml             # Project configuration
├── Dockerfile                 # Container build
├── docker-compose.yml         # Container orchestration
└── .github/workflows/ci.yml   # CI/CD pipeline
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.
