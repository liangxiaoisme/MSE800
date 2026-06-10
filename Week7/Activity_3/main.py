"""
Smart Office IoT Management System — Main Entry Point

Device IDs are auto-assigned by the system (0, 1, 2, ...).
"""
import sys
import os

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug.log")

def log(msg):
    """Write to both stdout and a log file so we can debug."""
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
        f.flush()

# Clear log
with open(LOG, "w", encoding="utf-8") as f:
    f.write("=== main.py started ===\n")

from factory import DeviceFactory
from config import ConfigurationManager


def show_table(devices):
    log(">>> show_table() called, len=" + str(len(devices)))
    if not devices:
        log(">>> No devices.")
        sys.stdout.write("\nNo devices.\n")
        sys.stdout.flush()
        return
    sys.stdout.write("\n" + "-" * 60 + "\n")
    sys.stdout.write(f"{'ID':<4} {'Device':<22} {'Location':<14} {'Power':<8} {'Status'}\n")
    sys.stdout.write("-" * 60 + "\n")
    for i, d in enumerate(devices):
        try:
            line = f"{i:<4} {d.device_type():<22} {d.location:<14} {d.power:<8} {d.detail()}"
        except Exception as e:
            line = f"{i:<4} [ERROR: {e}]"
        sys.stdout.write(line + "\n")
    sys.stdout.write("-" * 60 + "\n")
    sys.stdout.flush()
    log(">>> show_table() done")


def main():
    log("main() entered")
    sys.stdout.write("Welcome to the Office IoT Management System\n")
    sys.stdout.flush()

    cfg = ConfigurationManager()
    devices = []
    types = DeviceFactory.available_types()
    log("available types: " + str(types))

    while True:
        sys.stdout.write("\n1. Add Smart Device\n")
        sys.stdout.write("2. Display Device Status\n")
        sys.stdout.write("3. Configure Device\n")
        sys.stdout.write("4. Exit\n\n")
        sys.stdout.flush()

        try:
            choice = input("Select an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.stdout.write("\nGoodbye!\n")
            sys.stdout.flush()
            log("exit by EOF/KeyboardInterrupt")
            break

        log("user choice: |" + choice + "|")

        # -- 1. Add --
        if choice == "1":
            sys.stdout.write("\n")
            for i, t in enumerate(types):
                sys.stdout.write(f"  {i + 1}. {t.title()}\n")
            sys.stdout.flush()
            try:
                sel = int(input("Select device type (enter number): ").strip())
                if sel < 1 or sel > len(types):
                    sys.stdout.write("Invalid selection.\n")
                    sys.stdout.flush()
                    continue
                dtype = types[sel - 1]
            except ValueError:
                sys.stdout.write("Invalid selection.\n")
                sys.stdout.flush()
                continue

            loc = input("Enter location: ").strip()
            device = DeviceFactory.create(dtype, loc)
            if device:
                device.assign_id(len(devices))
                devices.append(device)
                sys.stdout.write(f"Device added successfully. Assigned ID: {device.device_id}\n")
                sys.stdout.flush()
                log("device added, count=" + str(len(devices)))
            else:
                sys.stdout.write("Failed to create device.\n")
                sys.stdout.flush()
                log("DeviceFactory.create returned None")

        # -- 2. Display --
        elif choice == "2":
            log(">>> entering branch 2")
            sys.stdout.write("[TRACE] You chose option 2\n")
            sys.stdout.flush()
            show_table(devices)
            log(">>> branch 2 done")

        # -- 3. Configure --
        elif choice == "3":
            log(">>> entering branch 3")
            if not devices:
                sys.stdout.write("\nNo devices to configure.\n")
                sys.stdout.flush()
                continue

            show_table(devices)

            try:
                idx = int(input("Enter the Device ID to edit: ").strip())
                d = devices[idx]
            except (ValueError, IndexError):
                sys.stdout.write("Invalid device ID.\n")
                sys.stdout.flush()
                continue

            sys.stdout.write(f"\nConfigure Device — {d.device_type()} [ID {d.device_id}]\n")
            sys.stdout.write("1. Turn On\n")
            sys.stdout.write("2. Turn Off\n")
            sys.stdout.write("3. Adjust Setting\n")
            sys.stdout.flush()

            c = input("Select Configure Option: ").strip()
            if c == "1":
                d.turn_on()
            elif c == "2":
                d.turn_off()
            elif c == "3":
                d.adjust_setting()
            else:
                sys.stdout.write("Invalid option.\n")
                sys.stdout.flush()
            log(">>> branch 3 done")

        # -- 4. Exit --
        elif choice == "4":
            sys.stdout.write("Goodbye!\n")
            sys.stdout.flush()
            log("normal exit")
            break

        else:
            sys.stdout.write("Invalid choice. Please enter 1-4.\n")
            sys.stdout.flush()
            log("invalid choice")


if __name__ == "__main__":
    main()
