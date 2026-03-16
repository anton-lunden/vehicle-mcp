from typing import Any

from aiohttp import ClientSession
from myskoda import MySkoda  # type: ignore[import-untyped]
from myskoda.models.info import CapabilityId  # type: ignore[import-untyped]

from vehicle_mcp.adapters.base import VehicleAdapter
from vehicle_mcp.adapters.vehicle_capability import VehicleCapability


class SkodaAdapter(VehicleAdapter):
    """Skoda vehicle adapter using myskoda library."""

    def __init__(
        self, username: str, password: str, vin: str | None = None, spin: str | None = None
    ):
        """Initialize Skoda adapter.

        Args:
            username: Skoda Connect username/email
            password: Skoda Connect password
            vin: Vehicle Identification Number (optional, uses first vehicle if not provided)
            spin: S-PIN for lock/unlock operations (optional)
        """
        self._username = username
        self._password = password
        self._vin = vin
        self._spin = spin
        self._myskoda: MySkoda | None = None
        self._session: ClientSession | None = None

    async def _ensure_connected(self) -> tuple[MySkoda, str]:
        """Ensure we have an active connection.

        Returns:
            A tuple of (MySkoda client, VIN string)
        """
        if self._myskoda is None:
            self._session = ClientSession()
            self._myskoda = MySkoda(self._session)
            await self._myskoda.connect(self._username, self._password)

            # If no VIN provided, get the first vehicle
            if self._vin is None:
                vins = await self._myskoda.list_vehicle_vins()
                if not vins:
                    raise ValueError("No vehicles found in account")
                self._vin = vins[0]

        if self._vin is None:
            raise RuntimeError("VIN was not set during connection")
        return self._myskoda, self._vin

    async def get_capabilities(self) -> VehicleCapability:
        """Detect supported capabilities from the Skoda API."""
        myskoda, vin = await self._ensure_connected()
        info = await myskoda.get_info(vin)

        features = VehicleCapability(0)

        if (
            info.has_capability(CapabilityId.CHARGING)
            or info.has_capability(CapabilityId.CHARGING_MEB)
            or info.has_capability(CapabilityId.CHARGING_MQB)
        ):
            features |= VehicleCapability.CHARGING

        if info.has_capability(CapabilityId.AIR_CONDITIONING):
            features |= VehicleCapability.CLIMATE

        if info.has_capability(CapabilityId.ACCESS):
            features |= VehicleCapability.LOCK

        return features

    async def get_vehicle_info(self) -> dict[str, Any]:
        """Get static vehicle information."""
        myskoda, vin = await self._ensure_connected()
        info = await myskoda.get_info(vin)

        result: dict[str, Any] = {
            "vin": vin,
            "brand": "Skoda",
        }

        if info.name:
            result["name"] = info.name

        if info.license_plate:
            result["license_plate"] = info.license_plate

        if info.software_version:
            result["software_version"] = info.software_version

        if info.specification:
            spec = info.specification
            if spec.model:
                result["model"] = spec.model
            if spec.title:
                result["title"] = spec.title
            if spec.model_year:
                result["model_year"] = spec.model_year
            if spec.manufacturing_date:
                result["manufacturing_date"] = spec.manufacturing_date.isoformat()
            if spec.body:
                result["body_type"] = spec.body.value
            if spec.trim_level:
                result["trim_level"] = spec.trim_level
            if spec.battery and spec.battery.capacity:
                result["battery_capacity_kwh"] = spec.battery.capacity
            if spec.max_charging_power:
                result["max_charging_power_kw"] = spec.max_charging_power
            if spec.engine:
                if spec.engine.power:
                    result["engine_power_kw"] = spec.engine.power
                if spec.engine.type:
                    result["engine_type"] = spec.engine.type

        return result

    async def get_vehicle_status(self) -> dict[str, Any]:
        """Get current vehicle status."""
        myskoda, vin = await self._ensure_connected()
        vehicle = await myskoda.get_vehicle(vin)

        result: dict[str, Any] = {}

        # Battery and range from charging
        if vehicle.charging:
            if vehicle.charging.status and vehicle.charging.status.battery:
                battery = vehicle.charging.status.battery
                if battery.state_of_charge_in_percent is not None:
                    result["state_of_charge_percent"] = battery.state_of_charge_in_percent
                if battery.remaining_cruising_range_in_meters is not None:
                    km = battery.remaining_cruising_range_in_meters / 1000.0
                    result["range_kilometers"] = km
                    result["range_miles"] = round(km * 0.621371, 1)

            if vehicle.charging.status:
                status = vehicle.charging.status
                if status.state:
                    result["charging_state"] = status.state.value
                if status.charge_power_in_kw is not None:
                    result["charge_power_kw"] = status.charge_power_in_kw
                if status.charging_rate_in_kilometers_per_hour is not None:
                    result["charging_rate_km_per_hour"] = (
                        status.charging_rate_in_kilometers_per_hour
                    )
                if status.remaining_time_to_fully_charged_in_minutes is not None:
                    result["minutes_to_fully_charged"] = (
                        status.remaining_time_to_fully_charged_in_minutes
                    )
                if status.charge_type:
                    result["charge_type"] = status.charge_type.value

            if vehicle.charging.settings:
                settings = vehicle.charging.settings
                if settings.target_state_of_charge_in_percent is not None:
                    result["target_state_of_charge_percent"] = (
                        settings.target_state_of_charge_in_percent
                    )

        # Location from positions
        if vehicle.positions and vehicle.positions.positions:
            pos = vehicle.positions.positions[0]
            if pos.gps_coordinates:
                result["latitude"] = pos.gps_coordinates.latitude
                result["longitude"] = pos.gps_coordinates.longitude
            if pos.address:
                addr = pos.address
                parts = []
                if addr.street:
                    parts.append(addr.street)
                if addr.city:
                    parts.append(addr.city)
                if addr.country:
                    parts.append(addr.country)
                if parts:
                    result["address"] = ", ".join(parts)

        # Door/window/lock status
        if vehicle.status:
            if vehicle.status.overall:
                overall = vehicle.status.overall
                if overall.locked is not None:
                    result["is_locked"] = overall.locked
                if overall.doors_locked is not None:
                    result["doors_locked"] = overall.doors_locked
                if overall.doors:
                    result["doors_open"] = overall.doors.value
                if overall.windows:
                    result["windows_open"] = overall.windows.value
                if overall.lights:
                    result["lights_on"] = overall.lights.value

            if vehicle.status.detail:
                detail = vehicle.status.detail
                if detail.bonnet:
                    result["bonnet_open"] = detail.bonnet.value
                if detail.trunk:
                    result["trunk_open"] = detail.trunk.value
                if detail.sunroof:
                    result["sunroof_open"] = detail.sunroof.value

            if vehicle.status.car_captured_timestamp:
                result["last_updated"] = vehicle.status.car_captured_timestamp.isoformat()

        # Air conditioning status
        if vehicle.air_conditioning:
            ac = vehicle.air_conditioning
            if ac.state:
                result["climate_control_state"] = ac.state.value
            if ac.target_temperature and ac.target_temperature.temperature_value is not None:
                result["climate_target_temperature_celsius"] = (
                    ac.target_temperature.temperature_value
                )
            if ac.seat_heating_activated:
                result["seat_heating_activated"] = True
            if ac.window_heating_enabled is not None:
                result["window_heating_enabled"] = ac.window_heating_enabled

        # Total range from driving range
        if vehicle.driving_range:
            if vehicle.driving_range.total_range_in_km is not None:
                result["total_range_kilometers"] = vehicle.driving_range.total_range_in_km

        # Health/maintenance
        if vehicle.health:
            if vehicle.health.mileage_in_km is not None:
                result["odometer_kilometers"] = vehicle.health.mileage_in_km

        return result

    async def start_climate_control(
        self, target_temperature: float, *, window_heating: bool = False
    ) -> bool:
        """Start climate control with target temperature in Celsius."""
        myskoda, vin = await self._ensure_connected()
        await myskoda.start_air_conditioning(vin, target_temperature)
        if window_heating:
            await myskoda.start_window_heating(vin)
        return True

    async def stop_climate_control(self) -> bool:
        """Stop climate control."""
        myskoda, vin = await self._ensure_connected()
        await myskoda.stop_air_conditioning(vin)
        return True

    async def start_charging(self, *, charge_limit_percent: int | None = None) -> bool:
        """Start charging the vehicle."""
        myskoda, vin = await self._ensure_connected()
        if charge_limit_percent is not None:
            await myskoda.set_charge_limit(vin, charge_limit_percent)
        await myskoda.start_charging(vin)
        return True

    async def stop_charging(self) -> bool:
        """Stop charging the vehicle."""
        myskoda, vin = await self._ensure_connected()
        await myskoda.stop_charging(vin)
        return True

    async def lock_vehicle(self) -> bool:
        """Lock the vehicle."""
        myskoda, vin = await self._ensure_connected()
        if not self._spin:
            raise ValueError("SECURE_PIN required for lock operation")
        await myskoda.lock(vin, self._spin)
        return True

    async def unlock_vehicle(self) -> bool:
        """Unlock the vehicle."""
        myskoda, vin = await self._ensure_connected()
        if not self._spin:
            raise ValueError("SECURE_PIN required for unlock operation")
        await myskoda.unlock(vin, self._spin)
        return True
