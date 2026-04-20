# Week 2 – Activity 1
# Basic Mathematical Operations with Complex Numbers

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

def modulus(x, y):
    return x % y

def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def power(x, y):
    return x ** y

def main():
    print("=== Simple Calculator ===")
    x = complex(input("Enter x: "))
    op = input("Operation (add/subtract/multiply/divide/mod/factorial/power): ")

    if op == "factorial":
        num = int(x.real)
        print(f"Factorial({num}) = {factorial(num)}")
        return

    y = complex(input("Enter y: "))

    if op == "add":
        print(f"{x} + {y} = {add(x, y)}")
    elif op == "subtract":
        print(f"{x} - {y} = {subtract(x, y)}")
    elif op == "multiply":
        print(f"{x} * {y} = {multiply(x, y)}")
    elif op == "divide":
        print(f"{x} / {y} = {divide(x, y)}")
    elif op == "mod":
        print(f"{x} % {y} = {modulus(x, y)}")
    elif op == "power":
        print(f"{x} ^ {y} = {power(x, y)}")
    else:
        print("Invalid operation")

if __name__ == "__main__":
    main()