import os
from nano_graphrag import GraphRAG
from nano_graphrag._storage import Neo4jStorage

neo4j_config = {
  "neo4j_url": os.environ.get("NEO4J_URL", "neo4j://localhost:7687"),
  "neo4j_auth": (
      os.environ.get("NEO4J_USER", "neo4j"),
      os.environ.get("NEO4J_PASSWORD", "neo4j"),
  )
}
GraphRAG(
  graph_storage_cls=Neo4jStorage,
  addon_params=neo4j_config,
)