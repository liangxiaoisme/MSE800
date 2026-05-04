class Land:
    """矩形土地类"""

    def __init__(self, length, width):
        # 保存土地的长和宽
        self.length = length
        self.width = width

    def get_area(self):
        """计算面积：长 × 宽"""
        return self.length * self.width

    def get_perimeter(self):
        """计算周长：2 × (长 + 宽)"""
        return 2 * (self.length + self.width)
