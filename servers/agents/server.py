from typing import Any

import aiohttp
from fastmcp import FastMCP
from loguru import logger

from settings import settings
from servers.agents import schemas


agents_mcp = FastMCP(name="AgentsServer")


async def _request(
    method: str,
    url: str,
    *,
    json: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
) -> Any:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, json=json, params=params) as response:
                try:
                    data = await response.json(content_type=None)
                except Exception:
                    data = await response.text()

                if response.status >= 400:
                    logger.error(f"Agents API error {response.status}: {data}")
                    return {
                        "is_error": True,
                        "status": response.status,
                        "response": data,
                    }

                return data
    except Exception as error:
        logger.error(f"Error occured with agents tool, {error}")
        return {
            "is_error": True,
            "status": None,
            "response": str(error),
        }


def _dump(item: Any) -> dict[str, Any]:
    return item.model_dump(mode="json", by_alias=True, exclude_none=True)


def _unwrap(data: Any, key: str) -> Any:
    if isinstance(data, dict) and data.get("is_error"):
        return data
    if isinstance(data, dict):
        return data.get(key, data)
    return data


@agents_mcp.tool
async def list_agents() -> list[schemas.AgentPayload] | dict:
    """Return all agents from the agents index."""
    logger.success("List agents tool used")
    data = await _request("get", settings.go_opensearch_database_agents_endpoint)
    return _unwrap(data, "agents")


@agents_mcp.tool
async def get_agent(uuid: str) -> schemas.AgentPayload | dict:
    """Return one agent by UUID."""
    logger.success(f"Get agent tool used, uuid: {uuid}")
    data = await _request(
        "get",
        f"{settings.go_opensearch_database_agent_endpoint}/{uuid}",
    )
    return _unwrap(data, "agent")


@agents_mcp.tool
async def create_agent(item: schemas.AgentWrite) -> str | dict:
    """Create an agent and return its generated UUID."""
    logger.success(f"Create agent tool used, name: {item.name}")
    return await _request(
        "post",
        settings.go_opensearch_database_agent_endpoint,
        json=_dump(item),
    )


@agents_mcp.tool
async def update_agent(uuid: str, item: schemas.AgentWrite) -> bool | dict:
    """Replace an agent by UUID."""
    logger.success(f"Update agent tool used, uuid: {uuid}")
    data = await _request(
        "put",
        f"{settings.go_opensearch_database_agent_endpoint}/{uuid}",
        json=_dump(item),
    )
    return _unwrap(data, "is_updated")


@agents_mcp.tool
async def patch_agent(uuid: str, item: schemas.AgentPatch) -> bool | dict:
    """Partially update an agent by UUID."""
    logger.success(f"Patch agent tool used, uuid: {uuid}")
    data = await _request(
        "patch",
        f"{settings.go_opensearch_database_agent_endpoint}/{uuid}",
        json=_dump(item),
    )
    return _unwrap(data, "is_updated")


@agents_mcp.tool
async def delete_agent(uuid: str) -> bool | dict:
    """Delete an agent by UUID."""
    logger.success(f"Delete agent tool used, uuid: {uuid}")
    data = await _request(
        "delete",
        f"{settings.go_opensearch_database_agent_endpoint}/{uuid}",
    )
    return _unwrap(data, "is_deleted")


@agents_mcp.tool
async def list_nodes() -> list[schemas.NodePayload] | dict:
    """Return all nodes from the nodes index."""
    logger.success("List nodes tool used")
    data = await _request("get", settings.go_opensearch_database_nodes_endpoint)
    return _unwrap(data, "nodes")


@agents_mcp.tool
async def get_node(uuid: str) -> schemas.NodePayload | dict:
    """Return one node by UUID."""
    logger.success(f"Get node tool used, uuid: {uuid}")
    data = await _request(
        "get",
        f"{settings.go_opensearch_database_node_endpoint}/{uuid}",
    )
    return _unwrap(data, "node")


@agents_mcp.tool
async def create_node(item: schemas.NodeWrite) -> str | dict:
    """Create a node and return its generated id."""
    logger.success(f"Create node tool used, name: {item.name}")
    return await _request(
        "post",
        settings.go_opensearch_database_node_endpoint,
        json=_dump(item),
    )


@agents_mcp.tool
async def update_node(uuid: str, item: schemas.NodeWrite) -> bool | dict:
    """Replace a node by UUID."""
    logger.success(f"Update node tool used, uuid: {uuid}")
    data = await _request(
        "put",
        f"{settings.go_opensearch_database_node_endpoint}/{uuid}",
        json=_dump(item),
    )
    return _unwrap(data, "is_updated")


@agents_mcp.tool
async def patch_node(uuid: str, item: schemas.NodePatch) -> bool | dict:
    """Partially update a node by UUID."""
    logger.success(f"Patch node tool used, uuid: {uuid}")
    data = await _request(
        "patch",
        f"{settings.go_opensearch_database_node_endpoint}/{uuid}",
        json=_dump(item),
    )
    return _unwrap(data, "is_updated")


@agents_mcp.tool
async def delete_node(uuid: str) -> bool | dict:
    """Delete a node by UUID."""
    logger.success(f"Delete node tool used, uuid: {uuid}")
    data = await _request(
        "delete",
        f"{settings.go_opensearch_database_node_endpoint}/{uuid}",
    )
    return _unwrap(data, "is_deleted")


@agents_mcp.tool
async def list_edges() -> list[schemas.EdgePayload] | dict:
    """Return all edges from the edges index."""
    logger.success("List edges tool used")
    data = await _request("get", settings.go_opensearch_database_edges_endpoint)
    return _unwrap(data, "edges")


@agents_mcp.tool
async def get_edge(uuid: str) -> schemas.EdgePayload | dict:
    """Return one edge by UUID."""
    logger.success(f"Get edge tool used, uuid: {uuid}")
    data = await _request(
        "get",
        f"{settings.go_opensearch_database_edge_endpoint}/{uuid}",
    )
    return _unwrap(data, "edge")


@agents_mcp.tool
async def create_edge(item: schemas.EdgeWrite) -> str | dict:
    """Create an edge and return its generated id."""
    logger.success(f"Create edge tool used, name: {item.name}")
    return await _request(
        "post",
        settings.go_opensearch_database_edge_endpoint,
        json=_dump(item),
    )


@agents_mcp.tool
async def update_edge(uuid: str, item: schemas.EdgeWrite) -> bool | dict:
    """Replace an edge by UUID."""
    logger.success(f"Update edge tool used, uuid: {uuid}")
    data = await _request(
        "put",
        f"{settings.go_opensearch_database_edge_endpoint}/{uuid}",
        json=_dump(item),
    )
    return _unwrap(data, "is_updated")


@agents_mcp.tool
async def patch_edge(uuid: str, item: schemas.EdgePatch) -> bool | dict:
    """Partially update an edge by UUID."""
    logger.success(f"Patch edge tool used, uuid: {uuid}")
    data = await _request(
        "patch",
        f"{settings.go_opensearch_database_edge_endpoint}/{uuid}",
        json=_dump(item),
    )
    return _unwrap(data, "is_updated")


@agents_mcp.tool
async def delete_edge(uuid: str) -> bool | dict:
    """Delete an edge by UUID."""
    logger.success(f"Delete edge tool used, uuid: {uuid}")
    data = await _request(
        "delete",
        f"{settings.go_opensearch_database_edge_endpoint}/{uuid}",
    )
    return _unwrap(data, "is_deleted")


@agents_mcp.tool
async def list_graphs() -> list[schemas.GraphPayload] | dict:
    """Return all graphs from the graphs index."""
    logger.success("List graphs tool used")
    data = await _request("get", settings.go_opensearch_database_graphs_endpoint)
    return _unwrap(data, "graphs")


@agents_mcp.tool
async def get_graph(uuid: str) -> schemas.GraphPayload | dict:
    """Return one graph by UUID."""
    logger.success(f"Get graph tool used, uuid: {uuid}")
    data = await _request(
        "get",
        f"{settings.go_opensearch_database_graph_endpoint}/{uuid}",
    )
    return _unwrap(data, "graph")


@agents_mcp.tool
async def get_full_graph(uuid: str) -> dict:
    """
    Return one graph with full node and edge objects.

    Use this before creating a similar graph when you need to inspect how an
    existing graph is wired: graph contains refs, nodes contain prompts/types,
    and edges contain source/target node ids.
    """
    logger.success(f"Get full graph tool used, uuid: {uuid}")
    graph_data = _unwrap(
        await _request(
            "get",
            f"{settings.go_opensearch_database_graph_endpoint}/{uuid}",
        ),
        "graph",
    )

    if isinstance(graph_data, dict) and graph_data.get("is_error"):
        return graph_data

    if not isinstance(graph_data, dict):
        return {
            "graph": graph_data,
            "nodes": [],
            "edges": [],
        }

    full_nodes = []
    for node_ref in graph_data.get("nodes", []) or []:
        if not isinstance(node_ref, dict) or not node_ref.get("id"):
            continue
        node_data = _unwrap(
            await _request(
                "get",
                f"{settings.go_opensearch_database_node_endpoint}/{node_ref['id']}",
            ),
            "node",
        )
        full_nodes.append(node_data)

    full_edges = []
    for edge_ref in graph_data.get("edges", []) or []:
        if not isinstance(edge_ref, dict) or not edge_ref.get("id"):
            continue
        edge_data = _unwrap(
            await _request(
                "get",
                f"{settings.go_opensearch_database_edge_endpoint}/{edge_ref['id']}",
            ),
            "edge",
        )
        full_edges.append(edge_data)

    return {
        "graph": graph_data,
        "nodes": full_nodes,
        "edges": full_edges,
    }


@agents_mcp.tool
async def create_graph(item: schemas.GraphWrite) -> str | dict:
    """Create a graph and return its generated id."""
    logger.success(f"Create graph tool used, name: {item.name}")
    return await _request(
        "post",
        settings.go_opensearch_database_graph_endpoint,
        json=_dump(item),
    )


@agents_mcp.tool
async def update_graph(uuid: str, item: schemas.GraphWrite) -> bool | dict:
    """Replace a graph by UUID."""
    logger.success(f"Update graph tool used, uuid: {uuid}")
    data = await _request(
        "put",
        f"{settings.go_opensearch_database_graph_endpoint}/{uuid}",
        json=_dump(item),
    )
    return _unwrap(data, "is_updated")


@agents_mcp.tool
async def patch_graph(uuid: str, item: schemas.GraphPatch) -> bool | dict:
    """Partially update a graph by UUID."""
    logger.success(f"Patch graph tool used, uuid: {uuid}")
    data = await _request(
        "patch",
        f"{settings.go_opensearch_database_graph_endpoint}/{uuid}",
        json=_dump(item),
    )
    return _unwrap(data, "is_updated")


@agents_mcp.tool
async def delete_graph(uuid: str) -> bool | dict:
    """Delete a graph by UUID."""
    logger.success(f"Delete graph tool used, uuid: {uuid}")
    data = await _request(
        "delete",
        f"{settings.go_opensearch_database_graph_endpoint}/{uuid}",
    )
    return _unwrap(data, "is_deleted")
