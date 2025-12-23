from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any

from orchestrator import app as graph_app   # your LangGraph compiled app


# ----------------------------
# FastAPI App
# ----------------------------
api = FastAPI(
    title="ABC Bank AI Risk & Compliance Orchestrator",
    description="Multi-Agent Banking Compliance Engine",
    version="1.0"
)


# ----------------------------
# CORS (Allow frontend)
# ----------------------------
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # for demo; later restrict domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Request Model
# ----------------------------
class OrchestratorRequest(BaseModel):
    user_input: str
    kyc_data: Optional[Dict[str, Any]] = None
    memory: Optional[list] = []


# ----------------------------
# Health Check
# ----------------------------
@api.get("/")
def health():
    return {"status": "OK", "message": "Banking AI Orchestrator Running"}


# ----------------------------
# MAIN PIPELINE RUNNER
# ----------------------------

@api.post("/run-orchestrator")
def run_orchestrator(request: OrchestratorRequest):
    state = {
        "user_input": request.user_input,
        "kyc_data": request.kyc_data or {
            "customer_name": "Unknown",
            "kyc_status": "UNKNOWN"
        },
        "memory": request.memory or []
    }

    result = graph_app.invoke(state)
    return result
