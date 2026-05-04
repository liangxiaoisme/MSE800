from land import Land


def main():
    # 获取用户输入的土地尺寸
    length = float(input("Enter the length: "))
    width = float(input("Enter the width: "))

    # 创建 Land 对象
    plot = Land(length, width)

    # 输出计算结果
    print("\nArea:", plot.get_area())
    print("Perimeter:", plot.get_perimeter())


if __name__ == "__main__":
    main()
