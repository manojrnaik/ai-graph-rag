from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field

class EntityNode(BaseModel):
    node_id: str = Field(..., description="Unique deterministic identifier (e.g., VENDOR_01, COMPONENT_XYZ)")
    label: Literal["COMPANY", "PERSON", "PRODUCT", "LOCATION", "LOGISTICS_BATCH"]
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Metadata key-value stores")

class GraphRelationship(BaseModel):
    source_id: str = Field(..., description="Origin node reference token")
    target_id: str = Field(..., description="Destination node reference token")
    relationship_type: Literal["MANUFACTURED_BY", "SHIPPED_VIA", "OWNED_BY", "LOCATED_IN"]
    weight: float = Field(default=1.0, description="Strength calculation rating of the graph link connection")

class KnowledgeGraphExtraction(BaseModel):
    extracted_nodes: List[EntityNode] = Field(default_factory=list)
    extracted_edges: List[GraphRelationship] = Field(default_factory=list)
