# Vehicle MCP Server

A Model Context Protocol (MCP) server for controlling your vehicle. Check battery status, control climate, lock/unlock doors, and more — from your AI assistant.

<img src="assets/demo.gif" width="400" height="401" alt="Demo">

**Supported brands:**

| Brand | Tools | Uses |
|-------|-------|------|
| Skoda | All | https://github.com/skodaconnect/myskoda |

**Tools:**

| Tool | Description |
|------|-------------|
| `get_vehicle_info` | Static vehicle info (VIN, model, year, etc.) |
| `get_vehicle_status` | Current status (battery, range, location, etc.) |
| `start_climate_control` | Start heating/cooling |
| `stop_climate_control` | Stop climate control |
| `start_charging` | Start charging |
| `stop_charging` | Stop charging |
| `lock_vehicle` | Lock vehicle |
| `unlock_vehicle` | Unlock vehicle |

## Installation

<details>
<summary>Claude Desktop</summary>

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vehicle": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "BRAND", "-e", "USERNAME", "-e", "PASSWORD", "ghcr.io/anton-lunden/vehicle-mcp"],
      "env": {
        "BRAND": "skoda",
        "USERNAME": "your-email@example.com",
        "PASSWORD": "your-password"
      }
    }
  }
}
```

</details>

<details>
<summary>Claude Code</summary>

```bash
claude mcp add vehicle \
  -e BRAND=skoda \
  -e USERNAME=your-email@example.com \
  -e PASSWORD=your-password \
  -- docker run -i --rm -e BRAND -e USERNAME -e PASSWORD ghcr.io/anton-lunden/vehicle-mcp
```

</details>

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `BRAND` | Yes | Vehicle brand (`skoda`) |
| `USERNAME` | Yes | Email for your vehicle's connected services (e.g., Skoda Connect) |
| `PASSWORD` | Yes | Password for your vehicle's connected services |
| `VIN` | No | Vehicle VIN (auto-detects if not set) |

### Skoda

| Variable | Required | Description |
|----------|----------|-------------|
| `SECURE_PIN` | For lock/unlock | S-PIN configured in Skoda Connect app |

## Multiple Vehicles

### Different accounts

If your vehicles are on separate accounts, just add multiple server entries. The VIN will be auto-detected:

```json
{
  "mcpServers": {
    "my-skoda": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "BRAND", "-e", "USERNAME", "-e", "PASSWORD", "ghcr.io/anton-lunden/vehicle-mcp"],
      "env": {
        "BRAND": "skoda",
        "USERNAME": "me@example.com",
        "PASSWORD": "my-password"
      }
    },
    "partners-skoda": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "BRAND", "-e", "USERNAME", "-e", "PASSWORD", "ghcr.io/anton-lunden/vehicle-mcp"],
      "env": {
        "BRAND": "skoda",
        "USERNAME": "partner@example.com",
        "PASSWORD": "their-password"
      }
    }
  }
}
```

### Same account

If you have multiple vehicles on the same account, specify the VIN for each:

```json
{
  "mcpServers": {
    "family-car": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "BRAND", "-e", "USERNAME", "-e", "PASSWORD", "-e", "VIN", "ghcr.io/anton-lunden/vehicle-mcp"],
      "env": {
        "BRAND": "skoda",
        "USERNAME": "me@example.com",
        "PASSWORD": "my-password",
        "VIN": "TMBXXXXXXXXXXXXXX"
      }
    },
    "weekend-car": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "BRAND", "-e", "USERNAME", "-e", "PASSWORD", "-e", "VIN", "ghcr.io/anton-lunden/vehicle-mcp"],
      "env": {
        "BRAND": "skoda",
        "USERNAME": "me@example.com",
        "PASSWORD": "my-password",
        "VIN": "TMBYYYYYYYYYYYYYYY"
      }
    }
  }
}
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
