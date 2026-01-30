# Contributing

## Adding a New Brand

1. Create `src/vehicle_mcp/adapters/yourbrand.py` implementing `VehicleAdapter`
2. Export in [`src/vehicle_mcp/adapters/__init__.py`](src/vehicle_mcp/adapters/__init__.py)
3. Add the brand to the selection logic in [`src/vehicle_mcp/server.py`](src/vehicle_mcp/server.py)

See [`src/vehicle_mcp/adapters/base.py`](src/vehicle_mcp/adapters/base.py) for the interface.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/anton-lunden/vehicle-mcp.git
cd vehicle-mcp

# Install dependencies
uv sync --dev

# Run linting
uv run ruff check .

# Run type checking
uv run pyrefly check src
```

## Running from Source

To test locally with e.g Claude Desktop, add to your `claude_desktop_config.json`:

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

## Code Style

- Format with `ruff format`
- Lint with `ruff check`
- Type check with `pyrefly`
