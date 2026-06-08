r"""
╔══════════════════════════════════════════════════════╗
║         欢迎使用 Smart Office IoT Management System        ║
║   Welcome to Smart Office IoT Management System     ║
╚══════════════════════════════════════════════════════╝

Reads user input, creates devices via DeviceFactory, and maintains one shared
ConfigurationManager (Singleton).
"""

from devices import SmartSwitch, SmartCurtain, SmartLock
from factory import DeviceFactory
from config import ConfigurationManager


def main():
    print("╔══════════════════════════════════════════════════════╗")
    print("║    欢迎使用 Smart Office IoT Management System      ║")
    print("║   Welcome to Smart Office IoT Management System     ║")
    print("╚══════════════════════════════════════════════════════╝")

    cfg = ConfigurationManager()
    devices = []

    menu = """
  ┌────────────────────────────────┐
  │  1. Add Device    添加设备      │
  │  2. Device Status  设备状态     │
  │  3. Configure Device  配置设备   │
  │  4. Exit  离开                  │
  └────────────────────────────────┘
  Choice / 选择: """

    while True:
        try:
            choice = input(menu).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        # ── 1. Add Device ──
        if choice == "1":
            print(f"\n  Available / 可用类型: {DeviceFactory.available_types()}")
            dtype = input("  Device type / 设备类型: ").strip().lower()
            if dtype not in DeviceFactory.available_types():
                print(f"  Unknown type '{dtype}'. Options: {DeviceFactory.available_types()}")
                continue
            did = input("  Device ID / 设备编号 (e.g. SW-001): ").strip()
            loc = input("  Location / 位置 (e.g. Office 3A): ").strip()
            device = DeviceFactory.create(dtype, did, loc)
            if device:
                devices.append(device)
                print(f"  ✓ {device.device_type()} '{did}' created at {loc}.")

        # ── 2. Device Status ──
        elif choice == "2":
            if not devices:
                print("\n  (No devices / 暂未添加设备)")
            else:
                print("\n  ════════ Device Status / 设备状态 ════════")
                for d in devices:
                    print(f"  • Name / 名称 : {d.device_type()}")
                    print(f"    Location / 位置 : {d.location}")
                    print(f"    Power / 电源   : {d.power}")
                    print(f"    State / 状态   : {d.detail()}")
                    print()
                print(f"  Total / 总数: {len(devices)} device(s)")

        # ── 3. Configure Device ──
        elif choice == "3":
            if not devices:
                print("\n  (No devices to configure / 暂无可配置设备)")
                continue
            print("\n  --- Select Device / 选择设备 ---")
            for i, d in enumerate(devices):
                print(f"  {i + 1}. {d.status()}")
            try:
                idx = int(input("  Number / 编号: ").strip()) - 1
                d = devices[idx]
            except (ValueError, IndexError):
                print("  Invalid selection.")
                continue

            if isinstance(d, SmartSwitch):
                print(f"\n  Configuring / 配置: SmartSwitch {d.device_id}")
                print(f"  Current / 当前: Power={d.power}, State={d.detail()}")
                print("  1. Turn ON / 开   2. Turn OFF / 关   3. Toggle / 切换")
                c = input("  Action / 操作: ").strip()
                if c == "1":
                    d.turn_on()
                elif c == "2":
                    d.turn_off()
                elif c == "3":
                    d.toggle()

            elif isinstance(d, SmartCurtain):
                print(f"\n  Configuring / 配置: SmartCurtain {d.device_id}")
                print(f"  Current / 当前: Power={d.power}, Open Level={d.open_level}%")
                print("  Enter openness percentage / 输入开合百分比 (0-100):")
                try:
                    pct = int(input("  Percentage / 百分比: ").strip())
                    d.set_level(pct)
                except ValueError:
                    print("  Invalid number.")

            elif isinstance(d, SmartLock):
                print(f"\n  Configuring / 配置: SmartLock {d.device_id}")
                print(f"  Current / 当前: Power={d.power}, State={d.detail()}")
                print("  1. Lock / 锁定   2. Unlock / 解锁")
                c = input("  Action / 操作: ").strip()
                if c == "1":
                    d.lock()
                elif c == "2":
                    d.unlock()

        # ── 4. Exit ──
        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("  Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
