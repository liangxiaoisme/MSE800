"""
IoT Smart Office — DeviceFactory (Factory Pattern)

The factory decouples device creation from client code. New device types can
be added by registering a new class — no existing code needs to change
(Open/Closed Principle).
"""

from devices import SmartSwitch, SmartCurtain, SmartLock


class DeviceFactory:
    """Creates device objects dynamically based on a type string."""

    _registry = {}

    @classmethod
    def register(cls, type_name, device_class):
        """Register a device class so the factory can create it."""
        cls._registry[type_name.lower()] = device_class

    @classmethod
    def create(cls, type_name, location):
        """Create and return a device instance, or None if type is unknown."""
        device_class = cls._registry.get(type_name.lower())
        if device_class is None:
            return None
        return device_class(location)

    @classmethod
    def available_types(cls):
        """Return all registered device type names."""
        return list(cls._registry.keys())


# Register the three concrete device types at module load time.
DeviceFactory.register("Smart Switch", SmartSwitch)
DeviceFactory.register("Smart Curtain", SmartCurtain)
DeviceFactory.register("Smart Lock", SmartLock)
