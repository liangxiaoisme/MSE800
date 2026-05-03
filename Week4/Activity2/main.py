"""
main.py

The main entry point for the Land Calculator application.
This module handles user input, creates a Rectangle object,
and displays the calculated area and perimeter.

Author: Student
Date: 2026-05-03
"""

from rectangle import Rectangle


def get_positive_number(prompt):
    """
    Prompt the user for a positive numeric value.

    This helper function repeatedly asks until a valid
    positive number is entered.

    Parameters:
        prompt (str): The message to display to the user.

    Returns:
        float: The validated positive number.
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  >> Error: Please enter a value greater than zero.")
                continue
            return value
        except ValueError:
            print("  >> Error: That is not a valid number. Please try again.")


def display_results(rectangle):
    """
    Display the area and perimeter of the given Rectangle.

    Parameters:
        rectangle (Rectangle): The Rectangle object to report on.
    """
    area = rectangle.calculate_area()
    perimeter = rectangle.calculate_perimeter()

    print("\n" + "=" * 50)
    print("          LAND CALCULATION RESULTS")
    print("=" * 50)
    print(f"  Dimensions:  Length = {rectangle.length} units")
    print(f"               Width  = {rectangle.width} units")
    print("-" * 50)
    print(f"  Area:        {area} square units")
    print(f"  Perimeter:   {perimeter} units")
    print("=" * 50)


def main():
    """
    Main program loop for the Land Calculator.

    Gathers user input, creates a Rectangle instance,
    and outputs the calculated measurements.
    """
    print("=" * 50)
    print("     RECTANGULAR LAND AREA & PERIMETER CALCULATOR")
    print("=" * 50)
    print("Enter the dimensions of your rectangular piece of land.\n")

    # Get validated user input for dimensions
    length = get_positive_number("Enter the length: ")
    width = get_positive_number("Enter the width:  ")

    # Create a Rectangle object (instance of the Rectangle class)
    land = Rectangle(length, width)

    # Display the calculated results
    display_results(land)

    print("\nThank you for using the Land Calculator!")


if __name__ == "__main__":
    main()
