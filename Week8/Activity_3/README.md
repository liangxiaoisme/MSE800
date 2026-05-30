# Week 8 - Activity 3: Single Inheritance / 单继承

**Air New Zealand Domestic Flight System / 新西兰航空 国内航班系统**

A small Python project demonstrating **single inheritance**.
一个演示**单继承**的小型 Python 项目。

`Flight` (parent / 父类)  →  `DomesticFlight` (child / 子类)

## Files / 文件

| File | Purpose / 用途 |
|------|----------------|
| `flight_system.py` | Parent class `Flight` + subclass `DomesticFlight` + demo / 父类、子类与演示 |
| `class_diagram.drawio` | UML class diagram, open with [draw.io](https://app.diagrams.net/) / 类图 |
| `class_diagram.puml` | Same diagram as PlantUML code / PlantUML 版类图 |
| `README.md` | This file / 本说明 |

## Class Design / 类设计

### Parent — `Flight` (generic flight / 通用航班)

**Attributes / 属性:** `airline` (class attr / 类属性), `flight_number`,
`origin`, `destination`, `capacity`, `base_fare`, `booked_seats`

**Methods / 方法:** `book_seat()`, `available_seats()`, `calculate_fare()`,
`get_flight_info()`

### Child — `DomesticFlight(Flight)` (domestic flight / 国内航班)

- **Inherited / 继承:** all attributes & methods above, reused via
  `super().__init__()` / 上述全部属性方法，通过 `super()` 复用
- **Extra attributes / 独有属性:** `GST_RATE` (15% NZ GST), `island`
- **Extra method / 独有方法:** `is_short_haul()`

## How inheritance is shown / 如何体现继承

1. `class DomesticFlight(Flight)` declares single inheritance / 声明单继承（仅一个父类）
2. `super().__init__(...)` reuses the parent constructor / 复用父类构造器，不重复写
3. The subclass reuses inherited methods (`book_seat`, `available_seats`) directly / 子类直接使用继承来的方法
4. The subclass adds its own attributes & method / 子类新增独有属性和方法

## Run / 运行

```bash
python flight_system.py
```

### Expected output / 预期输出

```
Air New Zealand NZ535: AKL->WLG | seats 4/4 | $138.00 | North Island [DOMESTIC]
Short-haul? True
Booking 1: OK
Booking 2: OK
Booking 3: OK
Booking 4: OK
Booking 5: FULL
Air New Zealand NZ535: AKL->WLG | seats 0/4 | $138.00 | North Island [DOMESTIC]
```

## Class Diagram / 类图

Open `class_diagram.drawio` in [draw.io](https://app.diagrams.net/) (or the
VS Code Draw.io extension). An empty-triangle arrow points from
`DomesticFlight` to `Flight`, denoting single inheritance.
用 draw.io 打开 `class_diagram.drawio`；空心三角箭头由子类指向父类，表示单继承。
