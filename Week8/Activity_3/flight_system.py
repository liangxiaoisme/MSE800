"""
Week 8 - Activity 3 / 第八周 活动三
Single Inheritance: Air New Zealand Domestic Flight System
单继承演示：新西兰航空 国内航班系统

Flight (parent / 父类)  ->  DomesticFlight (child / 子类)
"""


class Flight:
    """Generic flight = parent class. / 通用航班 = 父类。"""

    airline = "Air New Zealand"  # shared class attribute / 共享类属性（所有航班同一公司）

    def __init__(self, flight_number, origin, destination, capacity, base_fare):
        # Shared attributes, inherited by the subclass. / 共享属性，子类继承。
        self.flight_number = flight_number  # flight code / 航班号
        self.origin = origin                # from airport / 出发地
        self.destination = destination      # to airport / 目的地
        self.capacity = capacity            # total seats / 总座位数
        self.base_fare = base_fare          # base price NZD / 基础票价
        self.booked_seats = 0               # seats sold / 已售座位

    def book_seat(self):
        # Book one seat if not full. / 未满则订一个座位。
        if self.booked_seats < self.capacity:
            self.booked_seats += 1
            return True
        return False

    def available_seats(self):
        # Seats still free. / 剩余座位。
        return self.capacity - self.booked_seats

    def calculate_fare(self):
        # Base fare only; subclass extends this. / 仅基础票价；子类会扩展。
        return self.base_fare

    def get_flight_info(self):
        # One-line summary. / 一行摘要。
        return (f"{self.airline} {self.flight_number}: {self.origin}->{self.destination} "
                f"| seats {self.available_seats()}/{self.capacity} "
                f"| ${self.calculate_fare():.2f}")


class DomesticFlight(Flight):  # single inheritance: one parent / 单继承：只继承一个父类
    """Domestic flight = child class. / 国内航班 = 子类。"""

    GST_RATE = 0.15  # NZ GST / 新西兰商品服务税 15%

    def __init__(self, flight_number, origin, destination, capacity, base_fare, island):
        # Reuse parent to set shared attributes. / 调父类设置共享属性，避免重复。
        super().__init__(flight_number, origin, destination, capacity, base_fare)
        self.island = island  # extra attribute, child only / 子类独有属性（南/北岛）

    def calculate_fare(self):
        # Override: parent fare + GST. / 重写：父类票价基础上加 GST。
        return super().calculate_fare() * (1 + self.GST_RATE)

    def get_flight_info(self):
        # Override: parent info + island. / 重写：父类摘要再加岛屿信息。
        return f"{super().get_flight_info()} | {self.island} Island [DOMESTIC]"

    def is_short_haul(self):
        # Extra method, child only. / 子类独有方法：是否同岛短途。
        return self.island in ("North", "South")


if __name__ == "__main__":
    # Create a domestic flight (child object). / 创建国内航班（子类对象）。
    nz = DomesticFlight("NZ535", "AKL", "WLG", capacity=4, base_fare=120.0, island="North")

    print(nz.get_flight_info())                 # inherited+overridden / 继承并重写的方法
    print("Short-haul?", nz.is_short_haul())    # child-only method / 子类独有方法

    for i in range(5):                          # book_seat inherited / book_seat 继承自父类
        print(f"Booking {i + 1}:", "OK" if nz.book_seat() else "FULL")

    print(nz.get_flight_info())                 # after booking / 订座后再看
