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
