# Air New Zealand Flight Management System / 新西兰航空 航班管理系统

Week 8 - Activity 4 · A Python OOP project demonstrating **Hybrid Inheritance**.
第八周 活动四 · 一个演示**混合继承**的 Python 面向对象项目。

## Key Project Details / 项目概述

The system models flights along **two independent dimensions** and combines them
with hybrid inheritance (hierarchical **+** multiple).
系统沿**两个独立维度**对航班建模，并用混合继承（层次 **+** 多重）将其组合。

| Dimension / 维度 | Options / 取值 |
|---|---|
| **Type** / 类型 | Domestic 国内 · International 国际 |
| **Mode** / 方式 | Direct 直飞 · Transit 经停 |

`2 Types x 2 Modes` produces the four concrete flight classes the app runs.
`2 类型 × 2 方式` 得到程序实际使用的 4 个具体航班类。

## Core Components / 核心组成

The system uses **9 classes** in three layers / 系统分三层共 **9 个类**：

- **`Flight`** — base class holding data shared by every flight (route, baggage)
  and the methods `show_route`, `show_baggage`, `show_summary`. /
  基类，保存所有航班共有的数据与方法。
- **`DomesticFlight` / `InternationalFlight`** — child classes (hierarchical
  inheritance) adding type-specific rules: domestic check-in, international visa.
  / 子类（层次继承），分别加入国内值机、国际签证等规则。
- **`DirectFlight` / `TransitFlight`** — mixin classes for the travel mode; they
  do **not** inherit `Flight`, so the design stays free of any diamond/MRO trap.
  / 飞行方式的混入类，**不**继承 `Flight`，因此没有菱形/MRO 陷阱。
- **`DomesticDirectFlight`, `DomesticTransitFlight`, `InternationalDirectFlight`,
  `InternationalTransitFlight`** — combined classes (multiple inheritance), each
  inheriting **one Type + one Mode**. / 4 个组合类（多重继承），各继承"一个类型 +
  一个方式"。

## Main Functionality / 主要功能

- **Shared behaviour reuse / 共享行为复用:** route and baggage formatting are
  written once in `Flight` and reused by all subclasses. 航线与行李信息只在基类写一次，子类全部复用。
- **Type-specific rules / 类型专属规则:** domestic check-in info; international
  visa requirement. 国内值机信息；国际签证要求。
- **Mode-specific details / 方式专属信息:** direct = no stopover; transit = a
  stopover city and a transit boarding note. 直飞无经停；经停含经停地与中转提示。
- **Combined trip reports / 组合行程报告:** each combined class produces a
  `show_full_trip()` summary that merges information inherited from both parents.
  每个组合类的 `show_full_trip()` 汇总两个父类继承来的信息。

## How Hybrid Inheritance Is Shown / 如何体现混合继承

1. **Hierarchical / 层次:** `DomesticFlight(Flight)` and
   `InternationalFlight(Flight)` share one base class. 两个子类共享同一基类。
2. **Multiple / 多重:** e.g. `DomesticTransitFlight(DomesticFlight, TransitFlight)`
   inherits a Type and a Mode at once. 组合类同时继承一个类型和一个方式。
3. **Explicit constructors / 显式构造:** transit combos call both parents'
   `__init__` directly, so it is obvious which parent sets what. 经停组合类显式调用两个父类的
   `__init__`，谁初始化什么一目了然。

## Project Structure / 项目结构

| File / 文件 | Purpose / 用途 |
|---|---|
| `flight_system.py` | All 9 classes + the demo driver / 全部 9 个类与演示入口 |
| `class_diagram.drawio` | Coloured UML class diagram (open with [draw.io](https://app.diagrams.net/)) / 彩色类图 |
| `class_diagram.puml` | The same diagram as PlantUML code / PlantUML 版类图 |
| `README.md` | This file / 本说明 |

## Running the Application / 运行

Requires Python 3.x, no extra dependencies. / 需要 Python 3.x，无额外依赖。

```bash
python flight_system.py
```

### Expected output / 预期输出

```
=== Air New Zealand Flight Management System ===
NZ101: Auckland -> Wellington | Carry-on 7kg | Checked Depends on fare | Type: Domestic Direct | No stopover
NZ202: Auckland -> Queenstown | Carry-on 7kg | Checked Depends on fare | Stopover: Christchurch | Type: Domestic Transit | Check the next boarding gate during transit.
NZ289: Auckland -> Shanghai | Carry-on 7kg | Checked 2 x 23kg | Type: International Direct | Visa: Required | No stopover
NZ777: Auckland -> London | Carry-on 7kg | Checked 2 x 23kg | Stopover: Singapore | Type: International Transit | Visa: Required | Check the next boarding gate during transit.
```

## Class Diagram / 类图

Open `class_diagram.drawio` in [draw.io](https://app.diagrams.net/). Hollow
triangle arrows point from each child to its parent(s); every combined class has
**two** arrows — one to a Type class and one to a Mode mixin — which is the
multiple-inheritance half of the hybrid design. 用 draw.io 打开，空心三角箭头由子类指向父类，
每个组合类有**两条**箭头（分别指向类型类与方式混入类），即混合继承的多重继承部分。
```
                       Flight  (base / 基类)
                      /        \
            DomesticFlight   InternationalFlight     (hierarchical / 层次)
                      \        /
       DirectFlight / TransitFlight  (mixins / 混入，不继承 Flight)
                      \        /
   DomesticDirectFlight  DomesticTransitFlight
   InternationalDirectFlight  InternationalTransitFlight   (multiple / 多重)
```
