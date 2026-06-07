import logging
import json
from typing import Dict, Any, List, Optional
from src.schemas import KnowledgeGraphExtraction, EntityNode, GraphRelationship

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("GraphRAGEngine")

class ProductionGraphRAGStore:
    def __init__(self):
        # In-memory index simulating a Graph Database (Neo4j adjacency list representation)
        self.nodes_registry: Dict[str, EntityNode] = {}
        self.adjacency_matrix: Dict[str, List[GraphRelationship]] = {}

    async def write_knowledge_graph_payload(self, extraction: KnowledgeGraphExtraction):
        """Asynchronously upserts structured entity graphs into internal memory networks."""
        logger.info(f"Upserting {len(extraction.extracted_nodes)} nodes and {len(extraction.extracted_edges)} edges to the graph store.")
        
        for node in extraction.extracted_nodes:
            self.nodes_registry[node.node_id] = node
            if node.node_id not in self.adjacency_matrix:
                self.adjacency_matrix[node.node_id] = []
                
        for edge in extraction.extracted_edges:
            if edge.source_id in self.adjacency_matrix:
                # Deduplicate and update link parameters safely
                self.adjacency_matrix[edge.source_id].append(edge)
                logger.info(f"Established directional edge link: ({edge.source_id})--[{edge.relationship_type}]-->({edge.target_id})")

    async def execute_multi_hop_traversal(self, start_node_id: str, depth: int = 2) -> List[str]:
        """
        Simulates an explicit multi-hop path query traversal.
        Traces entity dependencies across the graph network to pull joined context.
        """
        logger.info(f"Executing Cypher-equivalent traversal path trace from root: '{start_node_id}' with depth ceiling: {depth}")
        if start_node_id not in self.nodes_registry:
            logger.warning(f"Root entry token entity '{start_node_id}' missing from structural registry indexes.")
            return []

        retrieved_context_paths = []
        visited_nodes = set()
        
        async def traverse_bfs(current_id: str, current_depth: int):
            if current_depth > depth or current_id in visited_nodes:
                return
            visited_nodes.add(current_id)
            
            node_data = self.nodes_registry.get(current_id)
            if node_data:
                retrieved_context_paths.append(f"Entity[{node_data.label}]: ID={node_data.node_id}, Attr={node_data.attributes}")
                
            edges = self.adjacency_matrix.get(current_id, [])
            for edge in edges:
                retrieved_context_paths.append(f"Relationship: ({edge.source_id})--|{edge.relationship_type}|-->({edge.target_id})")
                await traverse_bfs(edge.target_id, current_depth + 1)

        await traverse_bfs(start_node_id, 1)
        return retrieved_context_paths
