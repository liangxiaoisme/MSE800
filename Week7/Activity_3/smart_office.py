"""
Week 7 - Activity 3: IoT Smart Office Device Management System
Design Pattern: Factory Pattern (device creation) + Singleton (configuration manager)

Devices: SmartSwitch, SmartCurtain, SmartLock
The system creates device objects dynamically based on user input and maintains
only one ConfigurationManager instance for the entire application runtime.
"""

from abc import ABC, abstractmethod


# ===== DEVICES (Product hierarchy — Factory Pattern product side) =====

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
    def device_type(self):
        return "SmartSwitch"

    def toggle(self):
        """Extra method unique to switches — toggle on/off."""
        if self._status == "ON":
            self.turn_off()
        else:
            self.turn_on()


class SmartCurtain(Device):
    def device_type(self):
        return "SmartCurtain"

    def open(self):
        """Extra method unique to curtains — open the curtain."""
        self._status = "OPEN"
        print(f"  SmartCurtain {self.device_id} opened.")

    def close(self):
        """Extra method unique to curtains — close the curtain."""
        self._status = "CLOSED"
        print(f"  SmartCurtain {self.device_id} closed.")


class SmartLock(Device):
    def device_type(self):
        return "SmartLock"

    def lock(self):
        self._status = "LOCKED"
        print(f"  SmartLock {self.device_id} locked.")

    def unlock(self):
        self._status = "UNLOCKED"
        print(f"  SmartLock {self.device_id} unlocked.")


# ===== FACTORY (Factory Pattern — creator side) =====

class DeviceFactory:
    """Factory that creates Device objects dynamically based on type string.

    This is the core design pattern: the client never calls SmartSwitch() etc.
    directly — it asks the factory, which decides which concrete class to
    instantiate. New device types can be added by registering them without
    changing any client code (Open/Closed Principle).
    """

    _registry = {}  # device_type_string → Device subclass

    @classmethod
    def register(cls, type_name, device_class):
        """Register a device class so the factory knows how to create it."""
        cls._registry[type_name.lower()] = device_class

    @classmethod
    def create(cls, type_name, device_id, location):
        """Create and return a device instance by type name.

        Returns None if the type is not recognised.
        """
        device_class = cls._registry.get(type_name.lower())
        if device_class is None:
            return None
        return device_class(device_id, location)

    @classmethod
    def available_types(cls):
        """Return all registered device type names."""
        return list(cls._registry.keys())


# Register the three concrete device types so the factory can create them.
DeviceFactory.register("switch", SmartSwitch)
DeviceFactory.register("curtain", SmartCurtain)
DeviceFactory.register("lock", SmartLock)


# ===== SINGLETON (Configuration Manager) =====

class ConfigurationManager:
    """Singleton: only ONE instance exists for the entire application runtime.

    All parts of the system share the same configuration without passing it
    around — the class itself enforces the single-instance guarantee.
    """
    _instance = None   # class-level reference to the one and only instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._settings = {
                "system_name": "IoT Smart Office",
                "version": "1.0",
                "log_events": True,
            }
        return cls._instance

    def get(self, key, default=None):
        return self._settings.get(key, default)

    def set(self, key, value):
        self._settings[key] = value

    def show(self):
        print("\n  ⚙  Configuration Manager (Singleton)")
        for k, v in self._settings.items():
            print(f"     {k}: {v}")

    def is_same_instance(self, other):
        """Prove the Singleton is really one object."""
        return self is other


# ===== MAIN APPLICATION =====

def main():
    print("=" * 50)
    print("  IoT Smart Office Device Management System")
    print("=" * 50)

    # Demonstrate Singleton
    cfg1 = ConfigurationManager()
    cfg2 = ConfigurationManager()
    print(f"\n  Singleton proof: cfg1 is cfg2 → {cfg1.is_same_instance(cfg2)}")
    cfg1.show()

    devices = []  # store created devices

    menu = """
  ┌──────────────────────────────────┐
  │  1. Add a smart device           │
  │  2. List all devices             │
  │  3. Control a device             │
  │  4. Show configuration           │
  │  5. Exit                         │
  └──────────────────────────────────┘
  Choice: """

    while True:
        try:
            choice = input(menu).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if choice == "1":
            print(f"\n  Available types: {DeviceFactory.available_types()}")
            dtype = input("  Device type: ").strip().lower()
            if dtype not in DeviceFactory.available_types():
                print(f"  ✗ Unknown type '{dtype}'. Options: {DeviceFactory.available_types()}")
                continue
            did = input("  Device ID (e.g. SW-001): ").strip()
            loc = input("  Location (e.g. Office 3A): ").strip()
            device = DeviceFactory.create(dtype, did, loc)
            if device:
                devices.append(device)
                print(f"  ✓ {device.device_type()} {did} created at {loc}.")

        elif choice == "2":
            if not devices:
                print("\n  (no devices)")
            else:
                print("\n  --- Device List ---")
                for d in devices:
                    print(f"  {d.status()}")

        elif choice == "3":
            if not devices:
                print("\n  (no devices to control)")
                continue
            print("\n  --- Select Device ---")
            for i, d in enumerate(devices):
                print(f"  {i + 1}. {d.status()}")
            try:
                idx = int(input("  Number: ").strip()) - 1
                d = devices[idx]
            except (ValueError, IndexError):
                print("  ✗ Invalid selection.")
                continue
            # Show device-specific controls
            if isinstance(d, SmartSwitch):
                print("  1. Turn ON  2. Turn OFF  3. Toggle")
                c = input("  Action: ").strip()
                if c == "1": d.turn_on()
                elif c == "2": d.turn_off()
                elif c == "3": d.toggle()
            elif isinstance(d, SmartCurtain):
                print("  1. Open  2. Close")
                c = input("  Action: ").strip()
                if c == "1": d.open()
                elif c == "2": d.close()
            elif isinstance(d, SmartLock):
                print("  1. Lock  2. Unlock")
                c = input("  Action: ").strip()
                if c == "1": d.lock()
                elif c == "2": d.unlock()

        elif choice == "4":
            cfg1.show()
            print(f"\n  Devices stored: {len(devices)}")

        elif choice == "5":
            print("Bye!")
            break
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()
