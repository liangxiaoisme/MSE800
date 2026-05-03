"""
rectangle.py

This module defines the Rectangle class for the Land Calculator project.
It encapsulates the properties of a rectangular piece of land and
provides methods to calculate its area and perimeter.

Author: Student
Date: 2026-05-03
"""


class Rectangle:
    """
    A class to represent a rectangular piece of land.

    Attributes:
        length (float): The length of the rectangle.
        width (float): The width of the rectangle.
    """

    def __init__(self, length, width):
        """
        Initialise a Rectangle with given length and width.

        Parameters:
            length (float): The length dimension of the land.
            width (float): The width dimension of the land.

        Raises:
            ValueError: If length or width is negative or zero.
            TypeError: If length or width is not a number.
        """
        if not isinstance(length, (int, float)) or not isinstance(width, (int, float)):
            raise TypeError("Length and width must be numeric values.")
        if length <= 0 or width <= 0:
            raise ValueError("Length and width must be positive numbers greater than zero.")

        self.length = length
        self.width = width

    def calculate_area(self):
        """
        Calculate the area of the rectangular land.

        Formula: Area = length × width

        Returns:
            float: The area of the rectangle.
        """
        return self.length * self.width

    def calculate_perimeter(self):
        """
        Calculate the perimeter of the rectangular land.

        Formula: Perimeter = 2 × (length + width)

        Returns:
            float: The perimeter of the rectangle.
        """
        return 2 * (self.length + self.width)

    def __str__(self):
        """
        Return a human-readable string representation of the Rectangle.

        Returns:
            str: A formatted description of the rectangle's dimensions.
        """
        return f"Rectangle(length={self.length}, width={self.width})"

    def __repr__(self):
        """
        Return a formal string representation of the Rectangle.

        Returns:
            str: A string that could be used to recreate the object.
        """
        return f"Rectangle({self.length}, {self.width})"
