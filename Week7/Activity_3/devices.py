"""
IoT Smart Office — Device Classes (Product hierarchy)

All devices inherit from Device(ABC). IDs are auto-assigned by the system.
Each subclass implements device-specific state and control methods.
"""

from abc import ABC, abstractmethod


class Device(ABC):
    """Abstract base class for all smart office devices."""

    def __init__(self, location):
        self.location = location
        self.power = "OFF"

    def assign_id(self, n):
        """Called by main() after the device is created."""
        self._id = n

    @property
    def device_id(self):
        return self._id

    @abstractmethod
    def device_type(self):
        """Return the human-readable type name."""

    @abstractmethod
    def detail(self):
        """Return the Status column value."""

    def turn_on(self):
        self.power = "ON"
        print(f"  {self.device_type()} [ID {self._id}] turned ON.")

    def turn_off(self):
        self.power = "OFF"
        print(f"  {self.device_type()} [ID {self._id}] turned OFF.")

    @abstractmethod
    def adjust_setting(self):
        """Prompt user to set the device-specific value."""


class SmartSwitch(Device):
    def __init__(self, location):
        super().__init__(location)
        self._on = False

    def device_type(self):
        return "Smart Switch"

    def detail(self):
        return "ON" if self._on else "OFF"

    def turn_on(self):
        self.power = "ON"
        self._on = True
        print(f"  Smart Switch [ID {self._id}] turned ON.")

    def turn_off(self):
        self._on = False
        self.power = "OFF"
        print(f"  Smart Switch [ID {self._id}] turned OFF.")

    def adjust_setting(self):
        if self._on:
            self.turn_off()
        else:
            self.turn_on()


class SmartCurtain(Device):
    def __init__(self, location):
        super().__init__(location)
        self.position = 0

    def device_type(self):
        return "Smart Curtain"

    def detail(self):
        return f"position = {self.position}%"

    def turn_on(self):
        self.power = "ON"
        print(f"  Smart Curtain [ID {self._id}] turned ON.")

    def turn_off(self):
        self.power = "OFF"
        print(f"  Smart Curtain [ID {self._id}] turned OFF.")

    def adjust_setting(self):
        try:
            val = int(input("  Enter curtain position (0-100): ").strip())
            val = max(0, min(100, val))
            self.position = val
            self.power = "ON" if val > 0 else "OFF"
            print(f"  Smart Curtain [ID {self._id}] set to {val}%.")
        except ValueError:
            print("  Invalid input.")


class SmartLock(Device):
    def __init__(self, location):
        super().__init__(location)
        self._locked = True

    def device_type(self):
        return "Smart Lock"

    def detail(self):
        return "Locked" if self._locked else "Unlocked"

    def lock(self):
        self._locked = True
        self.power = "ON"
        print(f"  Smart Lock [ID {self._id}] locked.")

    def unlock(self):
        self._locked = False
        self.power = "OFF"
        print(f"  Smart Lock [ID {self._id}] unlocked.")

    def turn_on(self):
        self.lock()

    def turn_off(self):
        self.unlock()

    def adjust_setting(self):
        if self._locked:
            self.unlock()
        else:
            self.lock()
