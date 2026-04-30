# go-opensearch-rag-mcp-server

MCP-сервер на Python для работы с данными из `go-opensearch-database`.

Сервис объединяет несколько MCP-инструментов в одну точку входа и позволяет:

- получать текущее время;
- искать документы и фрагменты текста в OpenSearch;
- получать, записывать и удалять описания книг;
- получать список доступных индексов;
- создавать и обслуживать агентов, графы, узлы и ребра для агентных сценариев.

## Что внутри

Основной сервер запускается из [`main.py`](/c:/Users/Undefined/Documents/GitHub/go-opensearch-rag-mcp-server/main.py) и подключает четыре под-сервера:

- `search`:
  поиск документов и список книг в индексе;
- `descriptions`:
  чтение и изменение описаний книг;
- `resources`:
  доступ к списку индексов.
- `agents`:
  CRUD для agents/nodes/edges/graphs и последовательное создание графов агентом.

Транспорт запуска: `streamable-http`.

По умолчанию сервис слушает `0.0.0.0:13005`.

## MCP-инструменты

### Основной сервер

- `current_time() -> str`

### `search`

- `search_books(index: str)`  
  Возвращает список книг, загруженных в указанный индекс.
- `search_documents(item)`  
  Ищет документы по текстовому запросу.
- `search_documents_with_filter(item)`  
  Ищет документы с дополнительной фильтрацией по разрешенным и запрещенным книгам.

Фактические имена инструментов будут сформированы FastMCP с учетом префиксов, подключенных в [`main.py`](/c:/Users/Undefined/Documents/GitHub/go-opensearch-rag-mcp-server/main.py).

### `descriptions`

- `descriptions_get_all(index: str)`  
  Возвращает все описания книг в индексе.
- `descriptions_get_by_name(index: str, book_name: str)`  
  Возвращает описание конкретной книги.
- `descriptions_write(item)`  
  Создает или обновляет описание книги.
- `descriptions_delete(item)`  
  Удаляет описание книги.

### `resources`

- `resources_indexes()`  
  Возвращает список доступных индексов.

Дополнительно сервер публикует ресурс `resource://indexes`.

### `agents`

CRUD-инструменты:

- `agents_list_agents()`, `agents_get_agent(uuid)`, `agents_create_agent(item)`, `agents_update_agent(uuid, item)`, `agents_patch_agent(uuid, item)`, `agents_delete_agent(uuid)`
- `agents_list_nodes()`, `agents_get_node(uuid)`, `agents_create_node(item)`, `agents_update_node(uuid, item)`, `agents_patch_node(uuid, item)`, `agents_delete_node(uuid)`
- `agents_list_edges()`, `agents_get_edge(uuid)`, `agents_create_edge(item)`, `agents_update_edge(uuid, item)`, `agents_patch_edge(uuid, item)`, `agents_delete_edge(uuid)`
- `agents_list_graphs()`, `agents_get_graph(uuid)`, `agents_get_full_graph(uuid)`, `agents_create_graph(item)`, `agents_update_graph(uuid, item)`, `agents_patch_graph(uuid, item)`, `agents_delete_graph(uuid)`

Правила для LLM:

- `agent_type`: только `orchestrator` или `agent`;
- `model`: по умолчанию `openrouter::x-ai/grok-4.1-fast`;
- `agents`: обычно оставлять `[]`;
- `mcp_permissions`: router-сервисы `search`, `descriptions`, `agents`;
- `resources` не использовать в `mcp_permissions`;
- `node.type`: `INPUT` для входной ноды графа, обычно оркестратор; `CUSTOM` для промежуточной ноды; `OUTPUT` для финальной ноды;
- для агентного графа обычно создается несколько agents: каждая роль графа получает свой agent, а node ссылается на него через `agent_id`;
- граф создается только последовательными CRUD-вызовами: сначала `agents_create_agent`, затем `agents_create_node`, затем `agents_create_edge`, затем `agents_create_graph`;
- перед созданием агент должен проверить существующие agents/nodes/edges/graphs через list tools и не создавать дубли;
- если create возвращает только статус, id нужно получить через list tools: `agents_list_agents`, `agents_list_nodes`, `agents_list_edges`, `agents_list_graphs`;
- для новых объектов используйте уникальные имена с коротким run id, чтобы надежно найти созданный объект в list results;
- если list показывает уже существующий подходящий объект, агент может переиспользовать его вместо создания дубля;
- если нужно понять устройство существующего графа, использовать `agents_get_full_graph(uuid)`.

Упрощенный пример последовательного создания. Для реального агентного графа шаги `agents_create_agent` и `agents_create_node` повторяются для каждой роли графа.

```text
1. agents_create_agent({
  "item": {
    "name": "Rules Agent",
    "agent_description": "Answers questions using RAG tools.",
    "agent_type": "orchestrator",
    "model": "openrouter::x-ai/grok-4.1-fast",
    "system_prompt": "Use available MCP tools to answer accurately.",
    "agents": [],
    "mcp_permissions": ["search", "descriptions"]
  }
})

2. agents_create_node({
  "item": {
    "agent_id": "<agent_id from step 1>",
    "name": "Node Rules Orchestrator",
    "description": "Use available MCP tools to answer accurately.",
    "type": "INPUT"
  }
})

3. agents_create_edge({
  "item": {
    "from": "<source_node_id>",
    "to": "<target_node_id>",
    "name": "RulesOrchestrator-Searcher"
  }
})

4. agents_create_graph({
  "item": {
    "name": "RAG answer graph",
    "description": "Minimal graph for answering with retrieved context.",
    "nodes": [{"id": "<node_id>", "name": "Node Rules Orchestrator"}],
    "edges": [{"id": "<edge_id>", "name": "RulesOrchestrator-Searcher"}]
  }
})
```

## Зависимости

- Python `3.13`
- Poetry
- доступный HTTP API сервиса `go-opensearch-database`

Основные библиотеки:

- `fastmcp`
- `aiohttp`
- `loguru`
- `fastapi`

## Конфигурация

Настройки описаны в [`settings.py`](/c:/Users/Undefined/Documents/GitHub/go-opensearch-rag-mcp-server/settings.py).

Важно: сейчас `BaseSettings` по умолчанию читает файл `.env.production`.

Для локального запуска нужно либо:

1. заполнить `.env.production`,
2. либо изменить `env_file` в `settings.py`,
3. либо передать переменные окружения напрямую через среду выполнения.

Минимально необходимые переменные:

```env
HOST=0.0.0.0
PORT=13005
GO_OPENSEARCH_DATABASE_URL=http://localhost:8000
```

Также в настройках есть переменные для интеграционных тестов:

```env
TEST_PROVIDER_BASE_URL=
TEST_API_KEY=
TEST_MODEL_NAME=
TEST_MCP_URL=http://localhost:13005/mcp
```

## Установка и запуск

### Через Poetry

```bash
poetry install
poetry run python main.py
```

После запуска MCP-сервер будет доступен по адресу:

```text
http://localhost:13005/mcp
```

### Через Docker

```bash
docker build -t go-opensearch-rag-mcp-server .
docker run --rm -p 13005:13005 --env-file .env.production go-opensearch-rag-mcp-server
```

## Примеры сценариев использования

- получить список книг из индекса OpenSearch;
- найти релевантные фрагменты по пользовательскому запросу;
- ограничить поиск конкретными книгами;
- сохранить краткое описание книги для дальнейшего использования агентом;
- получить список индексов, доступных в базе.

## Тесты

В репозитории есть интеграционные тесты в [`servers/search/tool_test.py`](/c:/Users/Undefined/Documents/GitHub/go-opensearch-rag-mcp-server/servers/search/tool_test.py).

Для запуска тестов нужны:

- запущенный MCP-сервер;
- доступ к LLM-провайдеру;
- заполненные `TEST_*` переменные окружения.

Команда запуска:

```bash
poetry run pytest
```

## Структура проекта

```text
.
|-- main.py
|-- settings.py
|-- servers/
|   |-- search/
|   |-- descriptions/
|   |-- resourсes/
|   `-- agents/
|-- Dockerfile
`-- pyproject.toml
```
