# 🧩 Threat Model — RiskShield Security Playground

## 🎯 Scope
The **RiskShield app** is a demo web application built with Python/Streamlit (update if needed) and used as a **security playground** for SAST (Semgrep), DAST (OWASP ZAP), and AppSec automation.  

### System Components
- **Frontend / Static pages** → HTML templates served to end users
- **Backend APIs** → Python/FastAPI endpoints (`api.py`, `backend.py`)
- **Database / Storage** → Local storage or cloud data store (if configured)
- **Authentication** → Login/registration forms in `/static/`
- **Third-party integrations** → (e.g., OpenAI API, Firebase config)

---

## 🗺️ Data Flow Diagram (DFD)
```mermaid
flowchart LR
  U[User] -->|HTTP/HTTPS| FE[Frontend: Static HTML/Forms]
  FE --> API[Backend API: Python/FastAPI]
  API --> DB[(Database/Storage)]
  API --> EXT[External Services: OpenAI API, Firebase, etc.]


| Threat Category            | Description                              | Example in App                                     | Potential Impact                      | Mitigation                                  |
| -------------------------- | ---------------------------------------- | -------------------------------------------------- | ------------------------------------- | ------------------------------------------- |
| **Spoofing**               | Pretending to be another user or service | Weak login form in `static/login.html`             | Account takeover                      | Use MFA, secure session handling            |
| **Tampering**              | Modifying data or code                   | Unsanitized input passed to API                    | Data corruption, privilege escalation | Input validation, parameterized queries     |
| **Repudiation**            | Denying actions without audit trail      | No logging of login attempts                       | Difficult forensic analysis           | Centralized logging, signed logs            |
| **Information Disclosure** | Exposing sensitive data                  | Hardcoded API keys in HTML, verbose error messages | Credential theft, compliance risk     | Secrets in env vars, generic error messages |
| **Denial of Service**      | Overwhelming the app                     | Unthrottled login form                             | Service downtime                      | Rate limiting, WAF rules                    |
| **Elevation of Privilege** | Gaining more rights than intended        | Insecure role handling in backend                  | Unauthorized access                   | Enforce RBAC, secure session tokens         |
