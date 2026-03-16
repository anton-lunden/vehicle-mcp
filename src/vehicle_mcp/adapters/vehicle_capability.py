from enum import IntFlag, auto


class VehicleCapability(IntFlag):
    CHARGING = auto()
    CLIMATE = auto()
    LOCK = auto()
