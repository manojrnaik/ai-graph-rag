import asyncio
from src.schemas import KnowledgeGraphExtraction, EntityNode, GraphRelationship
from src.knowledge_graph import ProductionGraphRAGStore

async def main():
    # Instantiate the Graph Store Driver
    graph_rag_engine = ProductionGraphRAGStore()

    # Simulate structured output data arriving from document ingestion workers
    # Scenario text source: "Microchip Alpha-9 is manufactured by TaiwanSemi. Batch-4491 contains Alpha-9 and is shipped via DHL Blue."
    mock_extraction = KnowledgeGraphExtraction(
        extracted_nodes=[
            EntityNode(node_id="PROD_ALPHA9", label="PRODUCT", attributes={"name": "Alpha-9 Microchip", "tier": "Critical"}),
            EntityNode(node_id="COMP_TAIWANSEMI", label="COMPANY", attributes={"legal_name": "Taiwan Semiconductor Corp"}),
            EntityNode(node_id="BATCH_4491", label="LOGISTICS_BATCH", attributes={"storage_temp": "Ambient", "clearance": "Top Tier"}),
            EntityNode(node_id="LOG_DHL", label="COMPANY", attributes={"provider": "DHL Blue Logistics Hub"})
        ],
        extracted_edges=[
            GraphRelationship(source_id="PROD_ALPHA9", target_id="COMP_TAIWANSEMI", relationship_type="MANUFACTURED_BY"),
            GraphRelationship(source_id="BATCH_4491", target_id="PROD_ALPHA9", relationship_type="OWNED_BY"),
            GraphRelationship(source_id="BATCH_4491", target_id="LOG_DHL", relationship_type="SHIPPED_VIA")
        ]
    )

    print("--- STAGE 1: HYDRATING PRODUCTION GRAPH RELATIONSHIP STORES ---")
    await graph_rag_engine.write_knowledge_graph_payload(mock_extraction)

    print("\n--- STAGE 2: EXECUTING MULTI-HOP GRAPH-RAG RETRIEVAL QUERY ---")
    # Query intent simulation: Find everything related to BATCH_4491 up down the logistical path chain
    target_search_entity = "BATCH_4491"
    
    context_records = await graph_rag_engine.execute_multi_hop_traversal(
        start_node_id=target_search_entity, 
        depth=3
    )

    print(f"\n=== RETRIEVED GRAPHRAG CONTEXT INFRASTRUCTURE PAYLOAD ===")
    for idx, trace_record in enumerate(context_records, start=1):
        print(f"[{idx}] {trace_record}")

if __name__ == "__main__":
    asyncio.run(main())
