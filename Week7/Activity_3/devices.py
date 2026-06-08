"""
IoT Smart Office — Device Classes (Product hierarchy)

All three smart devices inherit from the abstract Device base class.
Each subclass adds device-specific control methods and state.
"""

from abc import ABC, abstractmethod


class Device(ABC):
    """Abstract base class for all smart office devices."""

    def __init__(self, device_id, location):
        self.device_id = device_id
        self.location = location
        self.power = "OFF"       # power state: ON / OFF

    @abstractmethod
    def device_type(self):
        """Return the human-readable type of this device."""

    @abstractmethod
    def detail(self):
        """Return the device-specific state string (e.g. 'ON', '60%', 'Locked')."""

    def status(self):
        """Full one-line status summary."""
        return f"[{self.device_type()}] {self.device_id} @ {self.location} | Power: {self.power} | State: {self.detail()}"

    def power_on(self):
        self.power = "ON"
        print(f"  {self.device_type()} {self.device_id} powered ON.")

    def power_off(self):
        self.power = "OFF"
        print(f"  {self.device_type()} {self.device_id} powered OFF.")


class SmartSwitch(Device):
    """Smart light switch: ON / OFF / toggle."""

    def __init__(self, device_id, location):
        super().__init__(device_id, location)
        self._on = False

    def device_type(self):
        return "SmartSwitch"

    def detail(self):
        return "ON" if self._on else "OFF"

    def turn_on(self):
        self.power = "ON"
        self._on = True
        print(f"  SmartSwitch {self.device_id} turned ON.")

    def turn_off(self):
        self._on = False
        if self.power == "ON":
            pass  # keep power on if other sub-devices use it
        print(f"  SmartSwitch {self.device_id} turned OFF.")

    def toggle(self):
        if self._on:
            self.turn_off()
        else:
            self.turn_on()


class SmartCurtain(Device):
    """Smart curtain: open level 0% (closed) to 100% (fully open)."""

    def __init__(self, device_id, location):
        super().__init__(device_id, location)
        self.open_level = 0     # 0 = fully closed, 100 = fully open

    def device_type(self):
        return "SmartCurtain"

    def detail(self):
        return f"{self.open_level}%"

    def set_level(self, percent):
        """Set curtain to a specific openness percentage (0-100)."""
        percent = max(0, min(100, percent))
        self.open_level = percent
        self.power = "ON" if percent > 0 else "OFF"
        print(f"  SmartCurtain {self.device_id} set to {percent}%.")


class SmartLock(Device):
    """Smart door lock: Locked / Unlocked."""

    def __init__(self, device_id, location):
        super().__init__(device_id, location)
        self._locked = True     # default: locked for security

    def device_type(self):
        return "SmartLock"

    def detail(self):
        return "Locked" if self._locked else "Unlocked"

    def lock(self):
        self._locked = True
        self.power = "ON"
        print(f"  SmartLock {self.device_id} locked.")

    def unlock(self):
        self._locked = False
        print(f"  SmartLock {self.device_id} unlocked.")
