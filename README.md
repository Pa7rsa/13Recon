# 🕶️ 13Recon

> Lightweight reconnaissance toolkit for authorized security research.

`13Recon` is a small, focused Python CLI for first-pass reconnaissance of a **domain you own or are explicitly authorized to test**.

It combines DNS resolution, HTTP/HTTPS probing, basic page metadata, security-header checks, and JSON reporting in one simple command.

## ✨ Features

- DNS `A`, `AAAA`, and `CNAME` lookups
- HTTP + HTTPS reachability checks
- Final URL, status code, title, server, content type, and redirect count
- Security-header presence checklist
- Concurrent HTTP checks
- JSON report export
- Input validation and bounded concurrency
- Automated tests + GitHub Actions CI
- Clean CLI designed for quick recon workflows

## ⚠️ Authorized Use Only

Use 13Recon only against systems you own, lab environments, or bug-bounty / security-testing targets where you have explicit permission to test.

The project is intentionally limited to low-impact reconnaissance helpers and does **not** attempt exploitation.

## 🚀 Quick Start

### Requirements

- Python 3.10+
- Internet access for live DNS/HTTP checks

### Install from source

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Run

```bash
13recon example.com
```

With custom timeouts and concurrency:

```bash
13recon example.com --timeout 8 --dns-timeout 4 --workers 10
```

Write a machine-readable report:

```bash
13recon example.com --json reports/example.json
```

## 🖥️ Example

```text
13Recon v0.2.0 :: authorized recon helper
Target: example.com

DNS
  A      93.184.216.34
  AAAA   -
  CNAME  -

HTTP
  http://example.com              200 Example Domain                       0.14s
  https://example.com             200 Example Domain                       0.16s

Security headers
  https://example.com
    strict-transport-security     MISSING
    content-security-policy       MISSING
    x-content-type-options        PRESENT
    x-frame-options               MISSING
    referrer-policy               MISSING
    permissions-policy            MISSING
```

*Example output is illustrative; live results vary by target.*

## 🧩 Project Layout

```text
13Recon/
├── src/
│   └── recon13/
│       ├── __init__.py
│       ├── cli.py
│       ├── dns.py
│       ├── http.py
│       └── models.py
├── tests/
│   ├── test_cli.py
│   └── test_http.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
└── pyproject.toml
```

## 🛠️ Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
ruff check .
```

## 🗺️ Roadmap

- [ ] Optional passive subdomain enumeration module
- [ ] Structured Markdown/HTML reports
- [ ] Pluggable reconnaissance checks
- [ ] Config file support
- [ ] Better terminal presentation
- [ ] G Society themed reporting

## 🕶️ 13 / G Society

`13` is the project's signature. The goal is to keep the identity recognizable without compromising the tool's practical security-research focus.

Part of the wider **G Society** identity.

## 📄 License

MIT — see [LICENSE](LICENSE).

---

### ⚡ Build. Research. Learn.
