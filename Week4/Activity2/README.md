# Rectangular Land Calculator

A simple Object-Oriented Programming (OOP) project that calculates the area and perimeter of a rectangular piece of land.

## Project Structure

```
land-calculator/
|-- rectangle.py     # Contains the Rectangle class
|-- main.py          # Entry point — handles user input and displays results
|-- README.md        # This documentation file
```

## Class Design

### `Rectangle` Class (`rectangle.py`)

| Attribute | Type  | Description                        |
|-----------|-------|-------------------------------------|
| `length`  | float | The length of the rectangle         |
| `width`   | float | The width of the rectangle          |

| Method                  | Returns | Description                          |
|-------------------------|---------|---------------------------------------|
| `calculate_area()`      | float   | Computes length x width              |
| `calculate_perimeter()` | float   | Computes 2 x (length + width)        |

The constructor (`__init__`) validates that both dimensions are positive numbers, raising descriptive errors for invalid input.

## How to Run

```bash
python main.py
```

You will be prompted to enter the length and width of your land. The program will then display the calculated area and perimeter.

## Example Output

```
==================================================
     RECTANGULAR LAND AREA & PERIMETER CALCULATOR
==================================================
Enter the dimensions of your rectangular piece of land.

Enter the length: 50
Enter the width:  30

==================================================
          LAND CALCULATION RESULTS
==================================================
  Dimensions:  Length = 50.0 units
               Width  = 30.0 units
--------------------------------------------------
  Area:        1500.0 square units
  Perimeter:   160.0 units
==================================================

Thank you for using the Land Calculator!
```

## OOP Concepts Demonstrated

- **Class** — `Rectangle` encapsulates data and behaviour
- **Attributes (instance variables)** — `length` and `width`
- **Methods** — `calculate_area()` and `calculate_perimeter()`
- **Encapsulation** — data validation inside the constructor
- **Modularity** — separate class module and main driver file
