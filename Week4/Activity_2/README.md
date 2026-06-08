# Land Calculator

A simple OOP project that calculates the area and perimeter of a rectangular piece of land.

## Files

| File | Description |
|------|-------------|
| `land.py` | Contains the `Land` class with `get_area()` and `get_perimeter()` methods |
| `main.py` | Entry point — gets user input, creates a `Land` object, and prints results |

## How to Run

```bash
python main.py
```

## Example Output

```
Enter the length: 50
Enter the width: 30

Area: 1500.0
Perimeter: 160.0
```

## OOP Features Used

- **Class**: `Land` — bundles data (length, width) and behaviour together
- **Instance variables**: `self.length`, `self.width` — store the object's data
- **Methods**: `get_area()` and `get_perimeter()` — perform calculations on the object's data
- **Modularity**: class definition and main program are in separate files
