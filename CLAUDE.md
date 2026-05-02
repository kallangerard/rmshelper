# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Flask API that acts as a bridge between [Current RMS](https://www.current-rms.com/) (rental management software) and Xero (accounting). It runs as an AWS Lambda function via Zappa.

Key workflows it automates:
- **Quick invoice**: creates an RMS invoice, posts it to Xero, strips zero-value line items (`quick_invoice`)
- **Global check-in**: finds all open opportunities containing a given asset barcode and checks them in (`global_check_in`)
- **Email invoice**: sends a Xero invoice via email

## Commands

```bash
# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Run locally
python app.py

# Run tests
pytest

# Run a single test
pytest tests/test_rmshelper.py::TestClass::test_one

# Lint
pylint rmshelper/

# Format
black .

# Deploy to AWS (requires zappa-admin AWS profile)
zappa deploy dev
zappa update dev
```

## Architecture

### `RMSManager` (rmshelper/rms.py)

Uses a metaclass-style pattern to dynamically generate HTTP methods at instantiation time. `MethodManager.__init__` iterates the `GET_DICTIONARY`, `POST_DICTIONARY`, and `PUT_DICTIONARY` dicts and calls `setattr(RMSManager, name, wrapper(...))` to attach methods like `get_opportunity`, `post_opportunities_quick_check_in`, etc.

The generated methods all share a single `MethodManager` instance's `self.url`, so the URL is baked in at method creation time. Calls like `r.get_opportunity(id=123)` use `self.url.format(id=...)` at call time.

`put_json` silently strips fields from `OPPORTUNITY_KEYS_TO_CLEAN` before every PUT — RMS returns 500 if those keys are present.

### `XeroRMS` (rmshelper/rmshelper.py)

Wraps `pyxero` with Xero Private App credentials (RSA key stored in AWS Secrets Manager). `clean_invoice` removes zero-value line items — Xero's API requires removing `TaxType`, `TaxAmount`, and `LineAmount` fields before a PUT will succeed.

### Secrets

Secrets are stored in AWS Secrets Manager under `{STAGE}/rmshelper` (JSON with `SUBDOMAIN`, `RMS_TOKEN`, `XERO_CONSUMER_KEY`) and `{STAGE}/xero` (raw RSA private key string). Required env vars: `STAGE`, `AWS_DEFAULT_REGION`.

Copy `.env.default` to `.env` and populate before running locally. The `STAGE` value determines which secrets are fetched.

### Deployment

Zappa deploys `app.app` as a Lambda function in `ap-southeast-2` using the `zappa-admin` AWS profile. The Lambda needs Secrets Manager read permissions (already configured in `zappa_settings.json`).

### Test fixtures

`tests/faker/` contains standalone scripts (not pytest fixtures) that hit the live Current RMS API to seed test data. They require `RMS_AUTH_TOKEN` and `RMS_SUBDOMAIN` env vars.
