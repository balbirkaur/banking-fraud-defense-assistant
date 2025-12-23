from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from fastapi import HTTPException

from orchestrator import app as graph_app
from agents.utils.customer_lookup import search_customers


api = FastAPI(
    title="ABC Bank AI Risk Orchestrator",
    description="Multi-Agent Banking Compliance Engine",
    version="1.0"
)


api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OrchestratorRequest(BaseModel):
    user_input: str
    kyc_data: Optional[Dict[str, Any]] = None
    memory: Optional[list] = []


@api.get("/")
def health():
    return {"status": "OK", "message": "Orchestrator Running"}


# =======================
#  SEARCH CUSTOMERS API
# =======================
@api.get("/search-customers")
def search(query: str):
    if len(query) < 3:
        raise HTTPException(status_code=400, detail="Query must be at least 3 characters")

    results = search_customers(query)

    if not results:
        return {"results": []}

    return {"results": results}


# =======================
# RUN MAIN PIPELINE
# =======================
@api.post("/run-orchestrator")
def run_orchestrator(request: OrchestratorRequest):

    if len(request.user_input.strip()) < 5:
        raise HTTPException(status_code=400, detail="User input too short")

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
