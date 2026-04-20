def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def calculate(a, b, op):
    if op == "*":
        return a * b
    elif op == " / ":
        return a / b
    elif op == " % ":
        return a % b
    
print("5 + 3 =", add(5, 3))
print("5 - 3 =", subtract(5, 3))
print("5 * 3 =", calculate(5, 3, "*"))
print("5 / 3 =", calculate(5, 3, " / "))
print("5 % 3 =", calculate(5, 3, " % "))