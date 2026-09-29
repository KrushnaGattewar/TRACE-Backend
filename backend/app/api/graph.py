"""
TRACE Intelligence Platform - Graph API
"""

from typing import List, Optional
from fastapi import APIRouter, Query
from app.schemas import GraphData
from app.graph.graph_service import graph_service

router = APIRouter(prefix="/graph", tags=["Graph Network"])

@router.get("", response_model=GraphData)
def get_graph():
    return graph_service.build_full_graph()

@router.get("/alert/{alert_id}", response_model=GraphData)
def get_alert_graph(alert_id: str):
    return graph_service.get_alert_investigation_graph(alert_id)

@router.get("/{entity_id}", response_model=GraphData)
def get_entity_graph(
    entity_id: str,
    hops: int = Query(2, ge=1, le=4, description="Number of hops to traverse"),
    entity_type: Optional[str] = Query(None, description="Comma separated entity types to include")
):
    types = [t.strip().upper() for t in entity_type.split(",")] if entity_type else None
    return graph_service.get_subgraph(entity_id, hops=hops, entity_types=types)

@router.get("/{entity_id}/neighbors", response_model=GraphData)
def get_entity_neighbors(
    entity_id: str,
    hops: int = Query(1, ge=1, le=3),
    only_suspicious: bool = Query(False)
):
    return graph_service.get_subgraph(entity_id, hops=hops, only_suspicious=only_suspicious)
