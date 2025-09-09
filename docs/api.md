# 📘 RiskShield API Reference

Welcome to the backend API documentation for the **RiskShield AI Security Assessment Platform**. This guide outlines the key endpoints, expected inputs, and response structures so frontend developers can integrate smoothly.

## Run API Server
```
uvicorn api:app --host 0.0.0.0 --port 8000 
```

---

## 🧭 API Base URL

```
http://localhost:8000
```

> If deployed to the cloud or containerized remotely, this URL may change to a public IP or domain.

---

## 🧪 Interactive API Docs (Swagger UI)

You can explore and test the API directly at:

```
http://localhost:8000/docs
```

---

## 📤 POST /upload/

Uploads a document (PDF, DOCX, or TXT), processes it, runs AI-based control assessments, generates a PDF report, and returns structured JSON results.

### 🔹 Request
**Method**: `POST`
**Endpoint**: `/upload/`
**Content-Type**: `multipart/form-data`

#### Form Field:
- `file`: the uploaded document file

### 🔹 Response
```json
{
  "message": "Document processed successfully",
  "report_file": "<filename>.pdf",
  "report_url": "<optional full blob URL>",
  "results": [
    {
      "Category": "Asset Management",
      "Question": "Do you maintain an inventory...?",
      "AI Response": "Yes, the documents show that...",
      "Rating": "Rating: Pass - Clear inventory evidence."
    }
  ]
}
```

### 🔹 Sample Frontend Code (JS/Fetch)
```javascript
const formData = new FormData();
formData.append("file", fileInput.files[0]);

fetch("http://localhost:8000/upload/", {
  method: "POST",
  body: formData,
})
  .then(res => res.json())
  .then(data => {
    console.log(data.report_url);
    console.log(data.results);
  });
```

---

## 📄 GET /report/{filename}

Downloads the generated assessment PDF report.

### 🔹 Request
**Method**: `GET`
**Endpoint**: `/report/{filename}`

### 🔹 Example
```
GET http://localhost:8000/report/f44ea0c7_report.pdf
```

### 🔹 Response
- A PDF file is returned for download if the file exists.

---

## 📦 Additional Endpoints

### ✅ Health Check
```http
GET /
```
Returns:
```json
{ "message": "Welcome to the RiskShield API" }
```

---

## 📁 Environment Variables
Make sure the following are set in `.env`:

```env
AZURE_STORAGE_CONNECTION_STRING=...
AZURE_STORAGE_ACCOUNT_NAME=...
```

---

## 🧼 Notes for Developers
- The API currently supports **one document upload per request**.
- Responses are AI-generated based on uploaded content and predefined control questions.
- If Azure upload is enabled, `report_url` will return a public or protected link.
- If you encounter a `NaN` or JSON error, the backend sanitizes those to ensure clean responses.

---

Let Amber know if you need support with mock data, CORS setup, or testing your frontend calls.

---

Built with ❤️ by the RiskShield backend team
