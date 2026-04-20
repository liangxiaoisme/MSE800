def math_operation(a, b, op):
    if op == "+":
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            return 'Error: Division by zero'
        return a / b
    elif op == '%':
        if b == 0:
            return 'Error: Modulo by zero'
        return a % b

def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def check_type(num):
    return type(num)

# 手动输入
num1 = complex(input("请输入第一个数（支持复数，如 2+3j）："))
num2 = complex(input("请输入第二个数（支持复数，如 4+1j）："))
op = input("请输入运算符(+, -, *, /, %)：")

# 输出结果
print("运算结果：", math_operation(num1, num2, op))

n = int(input("\n请输入一个整数计算阶乘："))
print(n, "! =", factorial(n))
print("数据类型：", check_type(num1))