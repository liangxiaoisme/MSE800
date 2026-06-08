# Week 7 — Activity 3: IoT Smart Office Device Management System

## Project Description

This project is an IoT-based smart office system that manages three types of
smart devices: **SmartSwitch**, **SmartCurtain**, and **SmartLock**. The system
creates device objects **dynamically at runtime** based on user input rather
than hard-coding device creation at compile time. It also ensures that only
**one configuration manager** exists for the entire application lifecycle.

### Design Patterns Used

#### 1. Factory Pattern (DeviceFactory)

The Factory Pattern is the core of this project. Instead of having client code
that calls `SmartSwitch()` or `SmartLock()` directly (which would make the code
rigid and hard to extend), we use a `DeviceFactory` that:

- **Registers** device types at startup (`DeviceFactory.register("switch", SmartSwitch)`)
- **Creates** device objects dynamically when the user provides a type string
  (`DeviceFactory.create("switch", "SW-001", "Office 3A")`)

**Why Factory?** Adding a new device type (e.g. `SmartLight`) requires only one
new class + one `register()` call. No existing client code needs to change.
This is the **Open/Closed Principle** — open for extension, closed for
modification.

#### 2. Singleton Pattern (ConfigurationManager)

The `ConfigurationManager` guarantees exactly one instance exists at any time.
`ConfigurationManager()` always returns the same object, proven by verifying
`cfg1 is cfg2` returns `True`.

**Why Singleton?** In an IoT system, a single configuration source (system name,
version, logging settings) prevents inconsistent state across the application.
All components read and write to the same configuration instance without
explicitly passing it around.

---

### OOP Concepts Demonstrated

| Concept | Where |
|---|---|
| **Abstract Base Class** | `Device(ABC)` — defines the contract that all devices must implement |
| **Polymorphism** | `device.status()` works on any device type; `DeviceFactory.create()` returns the right subclass |
| **Inheritance** | `SmartSwitch`, `SmartCurtain`, `SmartLock` all extend `Device` |
| **Encapsulation** | Internal state `_status` is protected; only exposed through methods |
| **Class-registry pattern** | `DeviceFactory._registry` maps type names to classes |

---

## Sample Output

```
==================================================
  IoT Smart Office Device Management System
==================================================

  Singleton proof: cfg1 is cfg2 → True

  ⚙  Configuration Manager (Singleton)
     system_name: IoT Smart Office
     version: 1.0
     log_events: True

  --- Device List ---
  [SmartSwitch] SW-001 @ Office 3A — ON
  [SmartCurtain] CT-002 @ Meeting Room B — OPEN
  [SmartLock] LK-003 @ Server Room — LOCKED
```

## Project Structure / 项目结构

```
Week7/Activity_3/
├── main.py        Entry point — CLI menu and application logic
├── devices.py     Device ABC + SmartSwitch, SmartCurtain, SmartLock
├── factory.py     DeviceFactory with class registry (Factory Pattern)
├── config.py      ConfigurationManager (Singleton Pattern)
└── README.md      This file
```

## Run / 运行

```bash
python main.py
```

No external dependencies — uses only Python standard library.
无需外部依赖 — 仅使用 Python 标准库。

## Menu

- **1. Add a smart device** — select type (switch/curtain/lock), enter ID and location
- **2. List all devices** — display status of every device
- **3. Control a device** — turn on/off, open/close, lock/unlock (device-specific actions)
- **4. Show configuration** — display the singleton ConfigurationManager settings
- **5. Exit**
