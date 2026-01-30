from abc import ABC, abstractmethod
from typing import Any


class VehicleAdapter(ABC):
    """Abstract base class for vehicle adapters.

    All vehicle brand adapters must implement this interface to provide
    a unified API for vehicle control regardless of the underlying client library.
    """

    @abstractmethod
    async def get_vehicle_info(self) -> dict[str, Any]:
        """Get static vehicle information.

        May include: vin, brand, model, display_name, year, color, etc.
        """
        ...

    @abstractmethod
    async def get_vehicle_status(self) -> dict[str, Any]:
        """Get current vehicle status.

        May include: state_of_charge_percent, range_kilometers, range_miles,
        latitude, longitude, odometer_kilometers, is_locked, is_charging, etc.
        """
        ...

    @abstractmethod
    async def start_climate_control(
        self, target_temperature: float, *, window_heating: bool = False
    ) -> bool:
        """Start climate control with target temperature in Celsius.

        Args:
            target_temperature: Target temperature in Celsius
            window_heating: Enable window heating/defrost
        """
        ...

    @abstractmethod
    async def stop_climate_control(self) -> bool:
        """Stop climate control."""
        ...

    @abstractmethod
    async def start_charging(self, *, charge_limit_percent: int | None = None) -> bool:
        """Start charging the vehicle.

        Args:
            charge_limit_percent: Optional charge limit (e.g., 80 for 80%)
        """
        ...

    @abstractmethod
    async def stop_charging(self) -> bool:
        """Stop charging the vehicle."""
        ...

    @abstractmethod
    async def lock_vehicle(self) -> bool:
        """Lock the vehicle."""
        ...

    @abstractmethod
    async def unlock_vehicle(self) -> bool:
        """Unlock the vehicle."""
        ...
