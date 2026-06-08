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
        self.power = "OFF"

    @abstractmethod
    def device_type(self):
        """Return the human-readable type of this device."""

    @abstractmethod
    def detail(self):
        """Return the device-specific state string for the Status column."""

    def turn_on(self):
        self.power = "ON"
        print(f"  {self.device_type()} {self.device_id} turned ON.")

    def turn_off(self):
        self.power = "OFF"
        print(f"  {self.device_type()} {self.device_id} turned OFF.")

    @abstractmethod
    def adjust_setting(self):
        """Prompt user to adjust the device-specific setting."""


class SmartSwitch(Device):
    """Smart light switch."""

    def __init__(self, device_id, location):
        super().__init__(device_id, location)
        self._on = False

    def device_type(self):
        return "Smart Switch"

    def detail(self):
        return "ON" if self._on else "OFF"

    def turn_on(self):
        self.power = "ON"
        self._on = True
        print(f"  Smart Switch {self.device_id} turned ON.")

    def turn_off(self):
        self._on = False
        self.power = "OFF"
        print(f"  Smart Switch {self.device_id} turned OFF.")

    def adjust_setting(self):
        if self._on:
            self.turn_off()
        else:
            self.turn_on()


class SmartCurtain(Device):
    """Smart curtain with percentage control."""

    def __init__(self, device_id, location):
        super().__init__(device_id, location)
        self.position = 0

    def device_type(self):
        return "Smart Curtain"

    def detail(self):
        return f"position = {self.position}%"

    def turn_on(self):
        self.power = "ON"
        print(f"  Smart Curtain {self.device_id} turned ON.")

    def turn_off(self):
        self.power = "OFF"
        print(f"  Smart Curtain {self.device_id} turned OFF.")

    def adjust_setting(self):
        try:
            val = int(input(f"  Enter curtain position (0-100): ").strip())
            val = max(0, min(100, val))
            self.position = val
            self.power = "ON" if val > 0 else "OFF"
            print(f"  Smart Curtain {self.device_id} set to {val}%.")
        except ValueError:
            print("  Invalid input.")


class SmartLock(Device):
    """Smart door lock."""

    def __init__(self, device_id, location):
        super().__init__(device_id, location)
        self._locked = True

    def device_type(self):
        return "Smart Lock"

    def detail(self):
        return "Locked" if self._locked else "Unlocked"

    def turn_on(self):
        self.lock()

    def turn_off(self):
        self.unlock()

    def lock(self):
        self._locked = True
        self.power = "ON"
        print(f"  Smart Lock {self.device_id} locked.")

    def unlock(self):
        self._locked = False
        self.power = "OFF"
        print(f"  Smart Lock {self.device_id} unlocked.")

    def adjust_setting(self):
        if self._locked:
            self.unlock()
        else:
            self.lock()
