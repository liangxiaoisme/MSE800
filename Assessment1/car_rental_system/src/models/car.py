"""
车辆领域模型 — 核心业务实体
"""

from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class GeoPoint:
    """地理位置值对象"""
    latitude: float
    longitude: float
    
    def is_valid(self) -> bool:
        return -90 <= self.latitude <= 90 and -180 <= self.longitude <= 180


@dataclass
class Car:
    """
    车辆实体 — 汽车租赁系统的核心领域对象
    
    Attributes:
        vehicle_id: 唯一车辆编号 (如 "NZ-AKL-2026-001")
        brand: 品牌 (如 "Toyota")
        model: 型号 (如 "Corolla")
        year: 生产年份
        mileage: 当前行驶里程（公里）
        available: 是否可用
        min_rental_days: 最短租赁天数
        max_rental_days: 最长租赁天数
        daily_rate: 日租金（NZD）
        health_score: 车辆健康评分 (0-100)
        current_location: 当前GPS位置
        last_telemetry_at: 最后遥测数据接收时间
    """
    
    vehicle_id: str
    brand: str
    model: str
    year: int
    mileage: int
    available: bool = True
    min_rental_days: int = 1
    max_rental_days: int = 30
    daily_rate: float = 50.0
    health_score: int = 100
    current_location: Optional[GeoPoint] = None
    last_telemetry_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def is_available_for(self, days: int) -> bool:
        """检查车辆是否满足指定租赁时长的可用性"""
        return (
            self.available and
            self.min_rental_days <= days <= self.max_rental_days and
            self.health_score >= 60  # 健康分过低不可出租
        )
    
    def update_mileage(self, new_mileage: int):
        """更新里程数，验证合理性"""
        if new_mileage < self.mileage:
            raise ValueError("新里程数不能小于当前里程")
        self.mileage = new_mileage
    
    def update_health_score(self, score: int):
        """更新健康评分"""
        self.health_score = max(0, min(100, score))
        if self.health_score < 60:
            self.available = False  # 自动下架
    
    def reserve(self):
        """预订车辆 — 锁定可用状态"""
        if not self.available:
            raise RuntimeError("车辆当前不可用")
        self.available = False
    
    def release(self):
        """释放车辆 — 恢复可用状态"""
        self.available = True
    
    def update_telemetry(self, location: GeoPoint, timestamp: datetime):
        """更新IoT遥测数据"""
        self.current_location = location
        self.last_telemetry_at = timestamp
    
    def to_dict(self) -> dict:
        return {
            "vehicle_id": self.vehicle_id,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "mileage": self.mileage,
            "available": self.available,
            "min_rental_days": self.min_rental_days,
            "max_rental_days": self.max_rental_days,
            "daily_rate": self.daily_rate,
            "health_score": self.health_score,
            "current_location": {
                "lat": self.current_location.latitude,
                "lng": self.current_location.longitude
            } if self.current_location else None,
            "last_telemetry_at": self.last_telemetry_at.isoformat() if self.last_telemetry_at else None
        }
