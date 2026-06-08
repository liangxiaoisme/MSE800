"""
IoT Smart Office Device Management System — Main Entry Point

Reads user input, creates devices via DeviceFactory, and maintains one shared
ConfigurationManager (Singleton).
"""

from devices import SmartSwitch, SmartCurtain, SmartLock
from factory import DeviceFactory
from config import ConfigurationManager


def main():
    print("=" * 50)
    print("  IoT Smart Office Device Management System")
    print("=" * 50)

    # Demonstrate Singleton: two "separate" calls return the exact same object.
    cfg1 = ConfigurationManager()
    cfg2 = ConfigurationManager()
    print(f"\n  Singleton proof: cfg1 is cfg2 → {cfg1 is cfg2}")
    cfg1.show()

    devices = []

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
