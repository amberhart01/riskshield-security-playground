from typing import List
from fastapi import FastAPI, UploadFile, File
from encryption_utils import encrypt_file
from cryptography.fernet import Fernet
from fastapi.responses import JSONResponse, FileResponse
from backend import load_file, chunk_docs, embed_docs, build_qa_chain, assess_controls, export_results_to_pdf
import shutil
import os
import pandas as pd
import uuid
import math
import traceback
from fastapi.middleware.cors import CORSMiddleware
from storage import upload_to_blob
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI()

ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY", Fernet.generate_key().decode())


class SurveyResponse(BaseModel):
    has_cyber_policy: bool
    uses_mfa: bool
    has_asset_inventory: bool
    has_incident_response_plan: bool
    business_size: str  # micro, small, medium
    has_security_staff: bool

CSF_TIERS = {
    "Tier 1": ["GV.OC", "ID.AM", "PR.AT", "PR.DS-11", "DE.CM-09"],
    "Tier 2": ["GV.RR", "ID.RA", "PR.AA", "PR.PS", "RS.MA"],
    "Tier 3": ["GV.SC", "PR.IR", "RS.CO", "RC.RP"],
    "Tier 4": ["GV.OV", "DE.AE", "RS.AN", "RC.CO"]
}

def determine_tier(resp: SurveyResponse) -> str:
    score = sum([
        resp.has_cyber_policy,
        resp.uses_mfa,
        resp.has_asset_inventory,
        resp.has_incident_response_plan,
        resp.has_security_staff
    ])
    if score <= 1:
        return "Tier 1"
    elif score == 2:
        return "Tier 2"
    elif score in [3, 4]:
        return "Tier 3"
    else:
        return "Tier 4"

@app.post("/survey")
def recommend_controls(response: SurveyResponse):
    tier = determine_tier(response)
    controls = CSF_TIERS.get(tier, [])
    return {"tier": tier, "recommended_controls": controls}


@app.get("/", response_class=HTMLResponse)
async def serve_home():
    with open("static/index.html", "r") as f:
        return f.read()

# Utility: clean NaN/inf from results
def sanitize_results(results):
    def sanitize_value(v):
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return None
        return v

    return [
        {k: sanitize_value(v) for k, v in row.items()}
        for row in results
    ]

from typing import List
from fastapi import UploadFile, File

@app.post("/upload")
async def upload_file(fileUpload: UploadFile = File(...)):
    os.makedirs("./uploads", exist_ok=True)  # Make sure upload dir exists


    filepath = f"./uploads/{fileUpload.filename}"
    file_bytes = await fileUpload.read()  # Read file contents from UploadFile
    encrypted_bytes = encrypt_file(file_bytes, ENCRYPTION_KEY.encode())

    with open(filepath, "wb") as f:
        f.write(encrypted_bytes)

    try:
        all_docs = load_file(filepath)
        chunks = chunk_docs(all_docs)
        vectordb = embed_docs(chunks)
        qa = build_qa_chain(vectordb)

        control_df = pd.read_excel("Template.xlsx", skiprows=3)
        control_df = control_df[["CATEGORY", "QUESTIONS"]].rename(
            columns={"CATEGORY": "Category", "QUESTIONS": "Question"}
        ).dropna(subset=["Question"]).ffill()

        results = assess_controls(qa, control_df)

        report_filename = f"/tmp/{uuid.uuid4()}_report.pdf"
        export_results_to_pdf(results, filename=report_filename)

        container_name = "reports"
        blob_name = os.path.basename(report_filename)
        upload_success = upload_to_blob(report_filename, container_name, blob_name)

        azure_url = (
            f"https://{os.getenv('AZURE_STORAGE_ACCOUNT_NAME')}.blob.core.windows.net/{container_name}/{blob_name}"
            if upload_success else None
        )

        cleaned_results = sanitize_results(results)

        return JSONResponse({
            "message": "Documents processed successfully",
            "report_file": blob_name,
            "report_url": azure_url,
            "results": cleaned_results
        })

    #except Exception as e:
     #   return JSONResponse(status_code=500, content={"error": str(e)})
    except Exception as e:
        error_message = str(e)
        error_trace = traceback.format_exc()
        print("Upload error:", error_message)
        print("Traceback:\n", error_trace)
        return JSONResponse(status_code=500, content={"error": error_message})

@app.get("/report/{filename}")
def download_report(filename: str):
    file_path = f"/tmp/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/pdf", filename=filename)
    return JSONResponse(status_code=404, content={"error": "Report not found"})

@app.get("/")
def root():
    return {"message": "Welcome to the RiskShield API"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Serve static HTML and assets
app.mount(
  "/", 
  StaticFiles(directory="static", html=True), 
  name="frontend"
)