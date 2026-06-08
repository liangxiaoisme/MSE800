"""
Smart Office IoT Management System — Main Entry Point

Reads user input, creates devices via DeviceFactory, and maintains one shared
ConfigurationManager (Singleton).
"""

from devices import SmartSwitch, SmartCurtain, SmartLock
from factory import DeviceFactory
from config import ConfigurationManager


def main():
    print("=" * 50)
    print("  Smart Office IoT Management System")
    print("=" * 50)

    cfg = ConfigurationManager()
    devices = []

    menu = """
  1. Add Device
  2. Device Status
  3. Configure Device
  4. Exit
  Choice: """

    while True:
        try:
            choice = input(menu).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        # -- 1. Add Device --
        if choice == "1":
            print(f"\n  Available types: {DeviceFactory.available_types()}")
            dtype = input("  Device type: ").strip().lower()
            if dtype not in DeviceFactory.available_types():
                print(f"  Unknown type '{dtype}'. Options: {DeviceFactory.available_types()}")
                continue
            did = input("  Device ID (e.g. SW-001): ").strip()
            loc = input("  Location (e.g. Office 3A): ").strip()
            device = DeviceFactory.create(dtype, did, loc)
            if device:
                devices.append(device)
                print(f"  {device.device_type()} '{did}' created at {loc}.")

        # -- 2. Device Status --
        elif choice == "2":
            if not devices:
                print("\n  (no devices)")
            else:
                print("\n  --- Device Status ---")
                for d in devices:
                    print(f"  Name    : {d.device_type()}")
                    print(f"  Location: {d.location}")
                    print(f"  Power   : {d.power}")
                    print(f"  State   : {d.detail()}")
                    print()
                print(f"  Total: {len(devices)} device(s)")

        # -- 3. Configure Device --
        elif choice == "3":
            if not devices:
                print("\n  (no devices to configure)")
                continue
            print("\n  --- Select Device ---")
            for i, d in enumerate(devices):
                print(f"  {i + 1}. {d.status()}")
            try:
                idx = int(input("  Number: ").strip()) - 1
                d = devices[idx]
            except (ValueError, IndexError):
                print("  Invalid selection.")
                continue

            if isinstance(d, SmartSwitch):
                print(f"\n  Configuring: SmartSwitch {d.device_id}")
                print(f"  Current: Power={d.power}, State={d.detail()}")
                print("  1. Turn ON  2. Turn OFF  3. Toggle")
                c = input("  Action: ").strip()
                if c == "1":
                    d.turn_on()
                elif c == "2":
                    d.turn_off()
                elif c == "3":
                    d.toggle()

            elif isinstance(d, SmartCurtain):
                print(f"\n  Configuring: SmartCurtain {d.device_id}")
                print(f"  Current: Power={d.power}, Open Level={d.open_level}%")
                print("  Enter openness percentage (0-100):")
                try:
                    pct = int(input("  Percentage: ").strip())
                    d.set_level(pct)
                except ValueError:
                    print("  Invalid number.")

            elif isinstance(d, SmartLock):
                print(f"\n  Configuring: SmartLock {d.device_id}")
                print(f"  Current: Power={d.power}, State={d.detail()}")
                print("  1. Lock  2. Unlock")
                c = input("  Action: ").strip()
                if c == "1":
                    d.lock()
                elif c == "2":
                    d.unlock()

        # -- 4. Exit --
        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("  Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
