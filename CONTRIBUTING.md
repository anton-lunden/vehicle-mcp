# Contributing

## Adding a New Brand

1. Create `src/vehicle_mcp/adapters/yourbrand.py` implementing `VehicleAdapter`
2. Export in [`src/vehicle_mcp/adapters/__init__.py`](src/vehicle_mcp/adapters/__init__.py)
3. Add the brand to the selection logic in [`src/vehicle_mcp/server.py`](src/vehicle_mcp/server.py)

See [`src/vehicle_mcp/adapters/base.py`](src/vehicle_mcp/adapters/base.py) for the interface.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/antonlunden/vehicle-mcp.git
cd vehicle-mcp

# Install dependencies
uv sync --dev

# Format and lint
uv run ruff format
uv run ruff check .

# Run type checking
uv run pyrefly check src
```

## Running from Source

To test locally, add to your MCP client configuration:

```json
{
  "mcpServers": {
    "vehicle": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/vehicle-mcp", "python", "-m", "vehicle_mcp"],
      "env": {
        "BRAND": "skoda",
        "USERNAME": "your-email@example.com",
        "PASSWORD": "your-password"
      }
    }
  }
}
```

To test the server directly from the terminal:

```bash
(printf '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1"}}}\n'; sleep 3; printf '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n'; sleep 1) | \
  env BRAND=skoda USERNAME=your-email@example.com PASSWORD=your-password uv run python -m vehicle_mcp
```

