"""
IoT Smart Office — Device Classes (Product hierarchy)

All three smart devices inherit from the abstract Device base class.
Each subclass adds device-specific control methods.
"""

from abc import ABC, abstractmethod


class Device(ABC):
    """Abstract base class for all smart office devices."""

    def __init__(self, device_id, location):
        self.device_id = device_id
        self.location = location
        self._status = "OFF"

    @abstractmethod
    def device_type(self):
        """Return the human-readable type of this device."""

    def status(self):
        return f"[{self.device_type()}] {self.device_id} @ {self.location} — {self._status}"

    def turn_on(self):
        self._status = "ON"
        print(f"  {self.device_type()} {self.device_id} turned ON.")

    def turn_off(self):
        self._status = "OFF"
        print(f"  {self.device_type()} {self.device_id} turned OFF.")


class SmartSwitch(Device):
    """Smart light switch: ON / OFF / toggle."""

    def device_type(self):
        return "SmartSwitch"

    def toggle(self):
        if self._status == "ON":
            self.turn_off()
        else:
            self.turn_on()


class SmartCurtain(Device):
    """Smart curtain: OPEN / CLOSED."""

    def device_type(self):
        return "SmartCurtain"

    def open(self):
        self._status = "OPEN"
        print(f"  SmartCurtain {self.device_id} opened.")

    def close(self):
        self._status = "CLOSED"
        print(f"  SmartCurtain {self.device_id} closed.")


class SmartLock(Device):
    """Smart door lock: LOCKED / UNLOCKED."""

    def device_type(self):
        return "SmartLock"

    def lock(self):
        self._status = "LOCKED"
        print(f"  SmartLock {self.device_id} locked.")

    def unlock(self):
        self._status = "UNLOCKED"
        print(f"  SmartLock {self.device_id} unlocked.")
