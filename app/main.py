"""
Mini SpecsComply Pro (SCP) - Document compliance and validation API.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(
    title="Mini SpecsComply Pro (SCP)",
    description="Document compliance and validation tool",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for demo (replace with DB/vector store in production)
documents: dict[str, dict] = {}


class UploadResponse(BaseModel):
    document_id: str
    message: str


class ComplianceIssue(BaseModel):
    section: str
    issue: str
    severity: str
    recommendation: str


class AnalysisResponse(BaseModel):
    document_id: str
    summary: str
    issues: list[ComplianceIssue]
    status: str


@app.get("/")
def root():
    return {"service": "Mini SpecsComply Pro (SCP)", "status": "running"}


@app.post("/upload-document", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload a document for compliance analysis. Returns document ID for tracking."""
    if not file.filename or not file.filename.lower().endswith((".docx", ".pdf", ".txt")):
        raise HTTPException(400, "Supported formats: .docx, .pdf, .txt")
    doc_id = str(uuid.uuid4())
    content = await file.read()
    documents[doc_id] = {
        "filename": file.filename,
        "content": content,
        "analysis": None,
    }
    return UploadResponse(document_id=doc_id, message="Document uploaded successfully")


@app.get("/document/{doc_id}/analysis", response_model=AnalysisResponse)
def get_document_analysis(doc_id: str):
    """Retrieve the compliance report for a document."""
    if doc_id not in documents:
        raise HTTPException(404, "Document not found")
    doc = documents[doc_id]
    if doc["analysis"] is None:
        # Placeholder until pipeline is wired (GROQ + Claude + Cohere)
        doc["analysis"] = {
            "summary": "Analysis pending. Wire GROQ/Claude/Cohere pipeline to generate report.",
            "issues": [],
            "status": "pending",
        }
    return AnalysisResponse(
        document_id=doc_id,
        summary=doc["analysis"]["summary"],
        issues=[ComplianceIssue(**i) for i in doc["analysis"].get("issues", [])],
        status=doc["analysis"]["status"],
    )


@app.post("/document/{doc_id}/resubmit", response_model=UploadResponse)
async def resubmit_document(doc_id: str, file: UploadFile = File(...)):
    """Resubmit a revised document for re-evaluation."""
    if doc_id not in documents:
        raise HTTPException(404, "Document not found")
    content = await file.read()
    documents[doc_id] = {
        "filename": file.filename or "resubmitted",
        "content": content,
        "analysis": None,
    }
    return UploadResponse(document_id=doc_id, message="Document resubmitted successfully")
