# Air New Zealand Flight Management System

Week 8 - Activity 4 · A Python OOP project demonstrating **Hybrid Inheritance**.

## Key Project Details

The system models flights along **two independent dimensions** and combines them
with hybrid inheritance (hierarchical **+** multiple).

| Dimension | Options |
|---|---|
| **Type** | Domestic · International |
| **Mode** | Direct · Transit |

`2 Types x 2 Modes` produces the four concrete flight classes the app runs.

## Core Components

The system uses **9 classes** in three layers:

- **`Flight`** — base class holding data shared by every flight (route, baggage)
  and the methods `show_route`, `show_baggage`, `show_summary`.
- **`DomesticFlight` / `InternationalFlight`** — child classes (hierarchical
  inheritance) adding type-specific rules: domestic check-in, international visa.
- **`DirectFlight` / `TransitFlight`** — mixin classes for the travel mode; they
  do **not** inherit `Flight`, so the design stays free of any diamond/MRO trap.
- **`DomesticDirectFlight`, `DomesticTransitFlight`, `InternationalDirectFlight`,
  `InternationalTransitFlight`** — combined classes (multiple inheritance), each
  inheriting **one Type + one Mode**.

## Main Functionality

- **Shared behaviour reuse:** route and baggage formatting are written once in
  `Flight` and reused by all subclasses.
- **Type-specific rules:** domestic check-in info; international visa requirement.
- **Mode-specific details:** direct = no stopover; transit = a stopover city and
  a transit boarding note.
- **Combined trip reports:** each combined class produces a `show_full_trip()`
  summary that merges information inherited from both parents.

## How Hybrid Inheritance Is Shown

1. **Hierarchical:** `DomesticFlight(Flight)` and `InternationalFlight(Flight)`
   share one base class.
2. **Multiple:** e.g. `DomesticTransitFlight(DomesticFlight, TransitFlight)`
   inherits a Type and a Mode at once.
3. **Explicit constructors:** transit combos call both parents' `__init__`
   directly, so it is obvious which parent sets what.

## Project Structure

| File | Purpose |
|---|---|
| `flight_system.py` | All 9 classes + the demo driver |
| `class_diagram.drawio` | Coloured UML class diagram (open with [draw.io](https://app.diagrams.net/)) |
| `class_diagram.puml` | The same diagram as PlantUML code |
| `README.md` | This file |

## Running the Application

Requires Python 3.x, no extra dependencies.

```bash
python flight_system.py
```

### Expected output

```
=== Air New Zealand Flight Management System ===
NZ101: Auckland -> Wellington | Carry-on 7kg | Checked Depends on fare | Type: Domestic Direct | No stopover
NZ202: Auckland -> Queenstown | Carry-on 7kg | Checked Depends on fare | Stopover: Christchurch | Type: Domestic Transit | Check the next boarding gate during transit.
NZ289: Auckland -> Shanghai | Carry-on 7kg | Checked 2 x 23kg | Type: International Direct | Visa: Required | No stopover
NZ777: Auckland -> London | Carry-on 7kg | Checked 2 x 23kg | Stopover: Singapore | Type: International Transit | Visa: Required | Check the next boarding gate during transit.
```

## Class Diagram

Open `class_diagram.drawio` in [draw.io](https://app.diagrams.net/). Hollow
triangle arrows point from each child to its parent(s); every combined class has
**two** arrows — one to a Type class and one to a Mode mixin — which is the
multiple-inheritance half of the hybrid design.

```
                       Flight  (base)
                      /        \
            DomesticFlight   InternationalFlight     (hierarchical)
                      \        /
       DirectFlight / TransitFlight  (mixins, not a Flight)
                      \        /
   DomesticDirectFlight  DomesticTransitFlight
   InternationalDirectFlight  InternationalTransitFlight   (multiple)
```
