# PreCog Deployment Risk Gate 🛡️

A lightweight, zero-overhead GitHub Action that audits changes and halts risky production deployments before they cause outages.

![Deployment Gate](https://img.shields.io/badge/Deployment%20Gate-Active-brightgreen)
![Risk Engine](https://img.shields.io/badge/PreCog-Engine%20v1.0-blue)

---

## ⚡ Why PreCog?

Traditional CI/CD pipelines either run every test blindly or let code ship directly. **PreCog Deployment Risk Gate** calculates an instant heuristic risk score based on context:
* 🔍 **Sensitive Paths:** Modifying critical systems (`auth`, `payment`, `database`, `secrets`).
* 🧪 **Test Parity Debt:** Catching critical path changes that lack accompanying test files.
* 🛑 **Fail-Fast Enforcement:** Terminates pipeline execution (`exit 1`) if the risk score crosses the configured threshold, skipping costly deployment steps.

---

## 🚀 Quickstart

Add this step directly before your production deployment command in `.github/workflows/deploy.yml`:

```yaml
name: Deploy Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 2  # Required to inspect the latest commit diff

      # 🛡️ Run PreCog Risk Gate
      - name: PreCog Deployment Risk Gate
        uses: yashasvibuilds/precog-risk-gate@v1
        with:
          risk-threshold: '60'  # Optional: default is 60

      # 🚀 Real Deployment (Runs only if risk score < threshold)
      - name: Deploy to Production
        run: |
          echo "Risk verification passed. Releasing to production..."
