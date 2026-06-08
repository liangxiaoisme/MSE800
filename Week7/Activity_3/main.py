"""
Smart Office IoT Management System — Main Entry Point

Reads user input, creates devices via DeviceFactory (Factory Pattern),
and maintains one shared ConfigurationManager (Singleton).
"""

from factory import DeviceFactory
from config import ConfigurationManager


def main():
    print("Welcome to the Office IoT Management System")

    cfg = ConfigurationManager()
    devices = []

    menu = "\n1. Add Smart Device\n2. Display Device Status\n3. Configure Device\n4. Exit\n\nSelect an option: "

    while True:
        try:
            choice = input(menu).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        # -- 1. Add Smart Device --
        if choice == "1":
            print(f"\nAvailable types: {DeviceFactory.available_types()}")
            dtype = input("Enter device type: ").strip()
            if dtype.lower() not in [t.lower() for t in DeviceFactory.available_types()]:
                print(f"Unknown type. Available: {DeviceFactory.available_types()}")
                continue
            did = input("Enter device ID (e.g. SW-001): ").strip()
            loc = input("Enter location: ").strip()
            device = DeviceFactory.create(dtype, did, loc)
            if device:
                devices.append(device)
                print(f"Device added successfully.")

        # -- 2. Display Device Status --
        elif choice == "2":
            if not devices:
                print("\nNo devices.")
            else:
                print("\n" + "-" * 60)
                print(f"{'ID':<4} {'Device':<22} {'Location':<14} {'Power':<8} {'Status'}")
                print("-" * 60)
                for i, d in enumerate(devices):
                    print(f"{i:<4} {d.device_type():<22} {d.location:<14} {d.power:<8} {d.detail()}")
                print("-" * 60)

        # -- 3. Configure Device --
        elif choice == "3":
            if not devices:
                print("\nNo devices to configure.")
                continue
            # Show table first so user can pick
            print("\n" + "-" * 60)
            print(f"{'ID':<4} {'Device':<22} {'Location':<14} {'Power':<8} {'Status'}")
            print("-" * 60)
            for i, d in enumerate(devices):
                print(f"{i:<4} {d.device_type():<22} {d.location:<14} {d.power:<8} {d.detail()}")
            print("-" * 60)

            try:
                idx = int(input("Enter the Device ID to edit: ").strip())
                d = devices[idx]
            except (ValueError, IndexError):
                print("Invalid device ID.")
                continue

            print(f"\nConfigure Device — {d.device_type()} ({d.device_id})")
            print("\n1. Turn On\n2. Turn Off\n3. Adjust Setting")
            c = input("Select Configure Option: ").strip()

            if c == "1":
                d.turn_on()
            elif c == "2":
                d.turn_off()
            elif c == "3":
                d.adjust_setting()
            else:
                print("Invalid option.")

        # -- 4. Exit --
        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
