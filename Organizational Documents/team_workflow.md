# 🧱 Shared Docker Workflow the Projects

## 🧰 Prerequisites
- Everyone has Docker installed locally.
- Everyone has access to your Azure Container Registry (ACR) (e.g., riskshieldacr).
- Project is version-controlled (GitHub, etc.).
- Shared .env file (but do not commit secrets — use .env.example as a template).

## 🔁 Team Workflow Overview
### ✅ 1. Pull latest code from Git
Before making changes:

```bash
git pull origin main
```

### ✅ 2. Make your code changes
Update files like `app.py`, `backend.py`, etc.

If you modify the `Dockerfile` or `requirements.txt`, alert the team.

### ✅ 3. Build your Docker image locally
```bash
docker build -t riskshieldacr.azurecr.io/myapp:<your_tag> .
```
Use a unique tag for each version (e.g., `myapp:v1.1`, `myapp:april-update`, etc.)
| 🔁 Consistent tagging prevents confusion and makes rollback easier.

### ✅ 4. Test your image locally
Use Docker Compose:
```bash
docker-compose up --build
```
Or run manually:

```bash
docker run -p 8501:8501 riskshieldacr.azurecr.io/myapp:<your_tag>
```

### ✅ 5. Log in to Azure Container Registry (ACR)

```bash
CopyEdit
az acr login --name riskshieldacr
```

### ✅ 6. Push the image to ACR

```bash
docker push riskshieldacr.azurecr.io/myapp:<your_tag>
```
| Make sure to push only tested and stable builds.
 
## 🌐 Deployment Workflow
### ✅ 7. Update Azure Web App to use new image tag
Go to Azure Portal → App Service → Configuration → Container settings
•	Change the tag under Image and tag from latest to your new tag (e.g., `myapp:april-update`)
•	Save and restart the Web App
🔁 If you're using `latest`, restarting the app should pull the newest build.
 
### 🧼 Optional Cleanup
After successful deployment, clean up old unused images locally:

```bash
docker image prune
```
 

