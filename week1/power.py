try:
    x = float(input("Enter the base (x): "))
    y = float(input("Enter the exponent (y): "))

    result = x ** y
    print("Result:", result)
except ValueError:
    print("Error: Please enter valid numbers!")