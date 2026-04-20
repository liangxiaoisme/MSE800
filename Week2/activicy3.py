class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b

    def power(self, a, b):
        return a ** b

    def factorial(self, n):
        res = 1
        for i in range(1, int(n)+1):
            res *= i
        return res


def get_num():
    return complex(input("Number: "))


def main():
    calc = Calculator()
    while True:
        print("\n1.add 2.subtract 3.multiply 4.divide 5.power 6.factorial 7.exit")
        c = input("Choice: ")

        if c in "12345":
            a = get_num()
            b = get_num()
            if c=="1": print(calc.add(a,b))
            elif c=="2": print(calc.subtract(a,b))
            elif c=="3": print(calc.multiply(a,b))
            elif c=="4": print(calc.divide(a,b))
            elif c=="5": print(calc.power(a,b))

        elif c=="6":
            n = int(get_num().real)
            print(calc.factorial(n))

        elif c=="7":
            break


if __name__ == "__main__":
    main()