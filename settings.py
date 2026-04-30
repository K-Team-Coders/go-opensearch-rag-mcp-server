from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(
        Path(__file__).parent.joinpath(".env.production")))

    # Service
    HOST: str = "0.0.0.0"
    PORT: int = 13005
    TEMP_DIRECTORY: Path = Path(__file__).parent.joinpath("tmp")

    # Go-opensearch-database
    GO_OPENSEARCH_DATABASE_URL: str
    GO_OPENSEARCH_DATABASE_BOOKS_LIST_ENDPOINT: str = "/api/v1/books/list"
    GO_OPENSEARCH_DATABASE_BOOKS_DESCRIPTIONS_ENDPOINT: str = "/api/v1/books/descriptions"
    GO_OPENSEARCH_DATABASE_BOOKS_DESCRIPTION_ENDPOINT: str = "/api/v1/books/description"
    GO_OPENSEARCH_DATABASE_SEARCH_DOCUMENTS_ENDPOINT: str = "/api/v1/search/documents"
    GO_OPENSEARCH_DATABASE_SEARCH_FILTER_DOCUMENTS_ENDPOINT: str = "/api/v1/search/filter_documents"
    GO_OPENSEARCH_DATABASE_INDEXES_ENDPOINT: str = "/api/v1/index-manager/indexes"
    GO_OPENSEARCH_DATABASE_AGENT_ENDPOINT: str = "/api/v1/agents/agent"
    GO_OPENSEARCH_DATABASE_AGENTS_ENDPOINT: str = "/api/v1/agents/agents"
    GO_OPENSEARCH_DATABASE_NODE_ENDPOINT: str = "/api/v1/agents/node"
    GO_OPENSEARCH_DATABASE_NODES_ENDPOINT: str = "/api/v1/agents/nodes"
    GO_OPENSEARCH_DATABASE_EDGE_ENDPOINT: str = "/api/v1/agents/edge"
    GO_OPENSEARCH_DATABASE_EDGES_ENDPOINT: str = "/api/v1/agents/edges"
    GO_OPENSEARCH_DATABASE_GRAPH_ENDPOINT: str = "/api/v1/agents/graph"
    GO_OPENSEARCH_DATABASE_GRAPHS_ENDPOINT: str = "/api/v1/agents/graphs"

    # Creds for tests
    TEST_PROVIDER_BASE_URL: Optional[str] = None
    TEST_API_KEY: Optional[str] = None
    TEST_MODEL_NAME: Optional[str] = None
    TEST_MCP_URL: Optional[str] = None

    @property
    def go_opensearch_database_books_list_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_BOOKS_LIST_ENDPOINT}"

    @property
    def go_opensearch_database_search_documents_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_SEARCH_DOCUMENTS_ENDPOINT}"

    @property
    def go_opensearch_database_search_filter_documents_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_SEARCH_FILTER_DOCUMENTS_ENDPOINT}"

    @property
    def go_opensearch_database_books_descriptions_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_BOOKS_DESCRIPTIONS_ENDPOINT}"

    @property
    def go_opensearch_database_books_description_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_BOOKS_DESCRIPTION_ENDPOINT}"

    @property
    def go_opensearch_database_indexes_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_INDEXES_ENDPOINT}"

    @property
    def go_opensearch_database_agent_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_AGENT_ENDPOINT}"

    @property
    def go_opensearch_database_agents_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_AGENTS_ENDPOINT}"

    @property
    def go_opensearch_database_node_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_NODE_ENDPOINT}"

    @property
    def go_opensearch_database_nodes_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_NODES_ENDPOINT}"

    @property
    def go_opensearch_database_edge_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_EDGE_ENDPOINT}"

    @property
    def go_opensearch_database_edges_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_EDGES_ENDPOINT}"

    @property
    def go_opensearch_database_graph_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_GRAPH_ENDPOINT}"

    @property
    def go_opensearch_database_graphs_endpoint(self) -> str:
        return f"{self.GO_OPENSEARCH_DATABASE_URL}{self.GO_OPENSEARCH_DATABASE_GRAPHS_ENDPOINT}"


settings = Settings()  # type: ignore
