import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from vehicle_mcp.adapters import SkodaAdapter

# Initialize from environment variables
BRAND = os.environ.get("BRAND")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
VIN = os.environ.get("VIN")  # Optional
SECURE_PIN = os.environ.get("SECURE_PIN")  # Optional

if not BRAND or not USERNAME or not PASSWORD:
    raise ValueError("Missing required environment variables: BRAND, USERNAME, PASSWORD")

BRAND = BRAND.lower()

if BRAND == "skoda":
    adapter = SkodaAdapter(
        username=USERNAME,
        password=PASSWORD,
        vin=VIN,
        spin=SECURE_PIN,
    )
else:
    raise ValueError(f"Unsupported brand: {BRAND}. Supported brands: skoda")

mcp = FastMCP("vehicle-mcp")


@mcp.tool()
async def get_vehicle_info() -> dict[str, Any]:
    """Get static vehicle information (model, brand, VIN)."""
    return await adapter.get_vehicle_info()


@mcp.tool()
async def get_vehicle_status() -> dict[str, Any]:
    """Get current vehicle status (battery, range, location)."""
    return await adapter.get_vehicle_status()


@mcp.tool()
async def start_climate_control(
    target_temperature_celsius: float = 21.0,
    window_heating: bool = False,
) -> dict[str, Any]:
    """Start climate control (heating/cooling).

    Args:
        target_temperature_celsius: Target temperature in Celsius (default: 21.0)
        window_heating: Enable window heating/defrost (default: False)
    """
    await adapter.start_climate_control(target_temperature_celsius, window_heating=window_heating)
    return {
        "status": "started",
        "target_temperature_celsius": target_temperature_celsius,
        "window_heating": window_heating,
    }


@mcp.tool()
async def stop_climate_control() -> dict[str, str]:
    """Stop climate control."""
    await adapter.stop_climate_control()
    return {"status": "stopped"}


@mcp.tool()
async def start_charging(charge_limit_percent: int | None = None) -> dict[str, Any]:
    """Start charging the vehicle.

    Args:
        charge_limit_percent: Optional charge limit (e.g., 80 for 80%)
    """
    await adapter.start_charging(charge_limit_percent=charge_limit_percent)
    result: dict[str, Any] = {"status": "charging"}
    if charge_limit_percent is not None:
        result["charge_limit_percent"] = charge_limit_percent
    return result


@mcp.tool()
async def stop_charging() -> dict[str, str]:
    """Stop charging the vehicle."""
    await adapter.stop_charging()
    return {"status": "stopped"}


@mcp.tool()
async def lock_vehicle() -> dict[str, str]:
    """Lock the vehicle. Requires SECURE_PIN to be configured."""
    await adapter.lock_vehicle()
    return {"status": "locked"}


@mcp.tool()
async def unlock_vehicle() -> dict[str, str]:
    """Unlock the vehicle. Requires SECURE_PIN to be configured."""
    await adapter.unlock_vehicle()
    return {"status": "unlocked"}


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
