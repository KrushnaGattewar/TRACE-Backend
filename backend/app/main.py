"""
TRACE Financial Crime & Insider Risk Intelligence Platform
FastAPI Application Entrypoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.alerts import router as alerts_router
from app.api.cases import router as cases_router
from app.api.graph import router as graph_router
from app.api.evidence import router as evidence_router
from app.api.entities import router as entities_router
from app.api.detection import router as detection_router

app = FastAPI(
    title="TRACE Financial Crime Intelligence Platform API",
    description="Explainable investigation graph, alert generation, and case management engine",
    version="1.0.0"
)

# Enable CORS for local Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(alerts_router)
app.include_router(cases_router)
app.include_router(graph_router)
app.include_router(evidence_router)
app.include_router(entities_router)
app.include_router(detection_router)

@app.get("/")
def root():
    return {
        "platform": "TRACE Financial Crime Intelligence Platform",
        "status": "OPERATIONAL",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
