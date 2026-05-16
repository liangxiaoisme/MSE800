"""
策略模式 — 租金计算引擎
将不同的定价算法封装为可互换的策略对象
"""

from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class PricingOptions:
    """定价上下文选项"""
    insurance_included: bool = False
    gps_included: bool = False
    child_seat_count: int = 0
    additional_driver: bool = False
    discount_rate: float = 0.0  # 0.0 ~ 1.0
    seasonal_multiplier: float = 1.0
    loyalty_tier: str = "bronze"  # bronze, silver, gold, platinum


class PricingStrategy(ABC):
    """定价策略抽象接口"""
    
    @abstractmethod
    def calculate(self, base_rate: Decimal, days: int, options: PricingOptions) -> Decimal:
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        pass


class StandardPricing(PricingStrategy):
    """
    标准计价策略
    公式: (基础日租 × 天数 + 附加费用) × 季节系数 × (1 - 折扣)
    """
    
    def calculate(self, base_rate: Decimal, days: int, options: PricingOptions) -> Decimal:
        # 基础租金
        subtotal = base_rate * days
        
        # 附加费用
        extras = Decimal("0.00")
        if options.insurance_included:
            extras += Decimal("25.00") * days  # 每日保险
        if options.gps_included:
            extras += Decimal("10.00") * days  # 每日GPS
        if options.child_seat_count > 0:
            extras += Decimal("8.00") * options.child_seat_count * days
        if options.additional_driver:
            extras += Decimal("15.00") * days
        
        # 季节调整 + 折扣
        total = (subtotal + extras) * Decimal(str(options.seasonal_multiplier))
        total = total * Decimal(str(1 - options.discount_rate))
        
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    def get_strategy_name(self) -> str:
        return "Standard Pricing"


class LuxuryPricing(PricingStrategy):
    """
    豪华车计价策略 — 豪华车溢价 + 强制全险
    公式: (基础日租 × 1.5 × 天数 + 强制保险 +  concierge) × 季节系数
    """
    
    LUXURY_MULTIPLIER = Decimal("1.5")
    CONCIERGE_FEE = Decimal("50.00")  # 每日礼宾服务费
    
    def calculate(self, base_rate: Decimal, days: int, options: PricingOptions) -> Decimal:
        # 豪华车基础溢价
        subtotal = base_rate * self.LUXURY_MULTIPLIER * days
        
        # 强制全险（不可取消）
        insurance = Decimal("45.00") * days
        
        # 礼宾服务
        concierge = self.CONCIERGE_FEE * days
        
        # GPS 免费
        extras = Decimal("0.00")
        if options.child_seat_count > 0:
            extras += Decimal("8.00") * options.child_seat_count * days
        if options.additional_driver:
            extras += Decimal("15.00") * days
        
        total = (subtotal + insurance + concierge + extras) * Decimal(str(options.seasonal_multiplier))
        
        # 豪华车也享受会员折扣
        loyalty_discount = self._get_loyalty_discount(options.loyalty_tier)
        total = total * Decimal(str(1 - loyalty_discount))
        
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    def _get_loyalty_discount(self, tier: str) -> float:
        discounts = {"bronze": 0.0, "silver": 0.05, "gold": 0.10, "platinum": 0.15}
        return discounts.get(tier, 0.0)
    
    def get_strategy_name(self) -> str:
        return "Luxury Pricing"


class LongTermPricing(PricingStrategy):
    """
    长租优惠策略 — 租赁 >= 7 天自动适用
    公式: 基础日租 × 天数 × 阶梯折扣
    """
    
    def calculate(self, base_rate: Decimal, days: int, options: PricingOptions) -> Decimal:
        # 长租阶梯折扣
        if days >= 30:
            discount = 0.25  # 月租 75折
        elif days >= 14:
            discount = 0.20  # 两周 8折
        elif days >= 7:
            discount = 0.10  # 周租 9折
        else:
            discount = 0.0
        
        subtotal = base_rate * days
        extras = self._calculate_extras(days, options)
        
        total = (subtotal + extras) * Decimal(str(1 - discount))
        
        # 可叠加会员折扣
        loyalty_discount = self._get_loyalty_discount(options.loyalty_tier)
        if loyalty_discount > 0:
            total = total * Decimal(str(1 - loyalty_discount))
        
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    def _calculate_extras(self, days: int, options: PricingOptions) -> Decimal:
        extras = Decimal("0.00")
        if options.insurance_included:
            extras += Decimal("20.00") * days  # 长租保险优惠
        if options.gps_included:
            extras += Decimal("10.00") * days
        if options.child_seat_count > 0:
            extras += Decimal("8.00") * options.child_seat_count * days
        return extras
    
    def _get_loyalty_discount(self, tier: str) -> float:
        discounts = {"bronze": 0.0, "silver": 0.03, "gold": 0.08, "platinum": 0.12}
        return discounts.get(tier, 0.0)
    
    def get_strategy_name(self) -> str:
        return "Long-Term Pricing"


class DynamicPricing(PricingStrategy):
    """
    动态定价策略（创新功能）— 基于实时供需调整
    公式: 基础日租 × 天数 × 动态供需系数 × 车辆健康系数
    """
    
    def __init__(self, demand_index: float = 1.0, vehicle_health: int = 100):
        self.demand_index = demand_index  # 0.5 ~ 3.0
        self.vehicle_health = vehicle_health
    
    def calculate(self, base_rate: Decimal, days: int, options: PricingOptions) -> Decimal:
        # 健康系数：健康分越低，价格越低（反映车况风险）
        health_multiplier = Decimal(str(max(0.8, self.vehicle_health / 100)))
        
        # 供需系数
        demand_multiplier = Decimal(str(self.demand_index))
        
        subtotal = base_rate * days * demand_multiplier * health_multiplier
        
        # 标准附加费用
        extras = Decimal("0.00")
        if options.insurance_included:
            extras += Decimal("25.00") * days
        if options.gps_included:
            extras += Decimal("10.00") * days
        
        total = subtotal + extras
        
        # 提前预订折扣
        if days >= 7:
            total = total * Decimal("0.95")  # 提前一周 95折
        
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    def get_strategy_name(self) -> str:
        return f"Dynamic Pricing (demand={self.demand_index}, health={self.vehicle_health})"


class PricingContext:
    """
    定价上下文 — 运行时选择和切换定价策略
    客户端代码只需与上下文交互，无需关心具体策略
    """
    
    def __init__(self, strategy: Optional[PricingStrategy] = None):
        self._strategy = strategy or StandardPricing()
    
    def set_strategy(self, strategy: PricingStrategy):
        self._strategy = strategy
    
    def calculate_price(self, base_rate: Decimal, days: int, options: PricingOptions) -> Decimal:
        return self._strategy.calculate(base_rate, days, options)
    
    def get_strategy_name(self) -> str:
        return self._strategy.get_strategy_name()
    
    @staticmethod
    def select_strategy(car_category: str, days: int, demand_index: float = 1.0) -> PricingStrategy:
        """
        智能策略选择器 — 根据车辆类型和租赁时长自动选择最优策略
        """
        if car_category in ("luxury", "sports", "suv_premium"):
            return LuxuryPricing()
        elif days >= 7:
            return LongTermPricing()
        elif demand_index != 1.0:
            return DynamicPricing(demand_index=demand_index)
        else:
            return StandardPricing()
