from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AgentType(str, Enum):
    AGENT = "agent"
    ORCHESTRATOR = "orchestrator"


class McpPermission(str, Enum):
    SEARCH = "search"
    DESCRIPTIONS = "descriptions"
    AGENTS = "agents"


ALLOWED_MCP_PERMISSIONS = {
    McpPermission.SEARCH.value,
    McpPermission.DESCRIPTIONS.value,
    McpPermission.AGENTS.value,
}


class AgentWrite(BaseModel):
    """Payload used to create or replace an agent."""

    name: str = Field(description="Agent display name.")
    agent_description: str = Field(description="What this agent is responsible for.")
    agent_type: AgentType = Field(
        description=(
            "Agent role. Use 'orchestrator' for the entry/manager agent that "
            "routes work through the graph. Use 'agent' for worker agents."
        ),
        examples=["orchestrator", "agent"],
    )
    model: str = Field(
        default="openrouter::x-ai/grok-4.1-fast",
        description=(
            "Model name used by the agent. Default is "
            "openrouter::x-ai/grok-4.1-fast."
        ),
        examples=["openrouter::x-ai/grok-4.1-fast"],
    )
    system_prompt: str = Field(description="System prompt for the agent.")
    agents: list[str] = Field(
        default_factory=list,
        description=(
            "Related agent ids. Leave this empty for automatic graph creation; "
            "routing is described by nodes and edges instead."
        ),
    )
    mcp_permissions: list[str] = Field(
        default_factory=list,
        description=(
            "Router services available to this agent. Allowed values are only "
            "'search', 'descriptions', and 'agents'. Do not use 'resources'; it "
            "is not an agent permission. Unknown values are ignored."
        ),
        examples=[["search"], ["search", "descriptions"], ["agents"]],
    )

    @field_validator("mcp_permissions", mode="before")
    @classmethod
    def normalize_mcp_permissions(cls, value: object) -> list[str]:
        if value is None:
            return []
        if not isinstance(value, list):
            return []

        normalized: list[str] = []
        for item in value:
            permission = str(item).strip()
            if permission in ALLOWED_MCP_PERMISSIONS and permission not in normalized:
                normalized.append(permission)

        return normalized


class AgentPatch(BaseModel):
    """Payload used to partially update an agent."""

    name: str | None = None
    agent_description: str | None = None
    agent_type: AgentType | None = None
    model: str | None = None
    system_prompt: str | None = None
    agents: list[str] | None = None
    mcp_permissions: list[str] | None = None

    @field_validator("mcp_permissions", mode="before")
    @classmethod
    def normalize_mcp_permissions(cls, value: object) -> list[str] | None:
        if value is None:
            return None
        return AgentWrite.normalize_mcp_permissions(value)


class AgentPayload(AgentWrite):
    """Agent object returned by the service."""

    uuid: str


class NodeType(str, Enum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    CUSTOM = "CUSTOM"


class NodeWrite(BaseModel):
    """Payload used to create or replace a node."""

    agent_id: str = Field(description="UUID of the parent agent.")
    name: str = Field(description="Node display name.")
    description: str = Field(
        description=(
            "Node behavior prompt or detailed role description. It can repeat the "
            "agent system prompt when the node represents that agent in the graph."
        ),
    )
    type: NodeType = Field(
        description=(
            "Graph node type. INPUT is the graph entry point, usually the "
            "orchestrator. CUSTOM is an intermediate worker node. OUTPUT is the "
            "terminal node, usually the finalizer that prepares the final answer."
        ),
        examples=["INPUT", "CUSTOM", "OUTPUT"],
    )


class NodePatch(BaseModel):
    """Payload used to partially update a node."""

    agent_id: str | None = None
    name: str | None = None
    description: str | None = None
    type: NodeType | None = None


class NodePayload(NodeWrite):
    """Node object returned by the service."""

    id: str


class EdgeWrite(BaseModel):
    """Payload used to create or replace an edge."""

    model_config = ConfigDict(populate_by_name=True)

    from_: str = Field(alias="from", description="Source node id.")
    to: str = Field(description="Destination node id.")
    name: str = Field(description="Edge display name.")


class EdgePatch(BaseModel):
    """Payload used to partially update an edge."""

    model_config = ConfigDict(populate_by_name=True)

    from_: str | None = Field(default=None, alias="from")
    to: str | None = None
    name: str | None = None


class EdgePayload(EdgeWrite):
    """Edge object returned by the service."""

    id: str


class NodeRef(BaseModel):
    id: str
    name: str


class EdgeRef(BaseModel):
    id: str
    name: str


class GraphWrite(BaseModel):
    """Payload used to create or replace a graph."""

    name: str = Field(description="Graph display name.")
    description: str = Field(description="Graph purpose.")
    nodes: list[NodeRef] = Field(default_factory=list)
    edges: list[EdgeRef] = Field(default_factory=list)


class GraphPatch(BaseModel):
    """Payload used to partially update a graph."""

    name: str | None = None
    description: str | None = None
    nodes: list[NodeRef] | None = None
    edges: list[EdgeRef] | None = None


class GraphPayload(GraphWrite):
    """Graph object returned by the service."""

    id: str
