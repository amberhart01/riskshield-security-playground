# 🛡️ RiskShield Security Playground

> Continuation of the RiskShield app as a **security testbed** to demonstrate AppSec practices:
> **Semgrep (SAST), OWASP ZAP (DAST), dependency audits, SBOM, and IaC checks**—with clear
> findings → fixes → re-scans.

**Original project:** (credit your teammates / class)  
**This repo:** Personal continuation focused on AppSec automation, threat modeling, and demos.

---

## ✨ Highlights
- Automated **Semgrep** scans on push/PR with SARIF results in *Code scanning alerts*
- On-demand **OWASP ZAP Baseline** DAST report against a running app URL
- **SBOM** (SPDX) + **dependency audit** for Python
- (Optional) **Terraform** security scanning (tfsec + Checkov) if/when IaC is added
- **Findings → fixes → re-scan** documented in `/docs`

---

## 📦 Tech & Tools
- **App:** Python (FastAPI/Streamlit) — update as appropriate
- **SAST:** Semgrep (community + audit profiles)
- **DAST:** OWASP ZAP Baseline
- **Deps/SBOM:** pip-audit, Anchore SBOM Action
- **IaC:** tfsec & Checkov (when Terraform modules are present)

---

## 🧪 CI Status
- Semgrep: ![Semgrep](https://github.com/amberhart01/riskshield-security-playground/actions/workflows/semgrep.yml/badge.svg)
- ZAP Baseline: ![ZAP Baseline](https://github.com/amberhart01/riskshield-security-playground/actions/workflows/zap-baseline.yml/badge.svg)
- Deps/SBOM: ![Deps & SBOM](https://github.com/amberhart01/riskshield-security-playground/actions/workflows/deps-sbom.yml/badge.svg)
- (Optional) IaC: ![IaC Security](https://github.com/amberhart01/riskshield-security-playground/actions/workflows/iac-security.yml/badge.svg)

---

## ▶️ Demos
Short videos and screenshots live under `/assets/` and on my portfolio page.  
*(Keep videos <100MB or host externally and embed)*

```html
<video controls width="720" poster="/assets/images/demo-thumb.png">
  <source src="/assets/videos/riskshield-demo.mp4" type="video/mp4">
</video>
```
> **Note:** This repository and its contents are for demonstration purposes only.
> No live systems, secrets, or production data are included.
