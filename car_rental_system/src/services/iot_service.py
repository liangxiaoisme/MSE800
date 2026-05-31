"""
创新功能：IoT 车辆遥测服务
实现预测性维护、实时健康监测与地理围栏
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from enum import Enum
import statistics


class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class GeoPoint:
    latitude: float
    longitude: float


@dataclass
class GeoPolygon:
    """多边形地理围栏"""
    points: List[GeoPoint]
    
    def contains(self, point: GeoPoint) -> bool:
        """射线法判断点是否在多边形内"""
        n = len(self.points)
        inside = False
        p1x, p1y = self.points[0].latitude, self.points[0].longitude
        for i in range(1, n + 1):
            p2x, p2y = self.points[i % n].latitude, self.points[i % n].longitude
            if point.longitude > min(p1y, p2y):
                if point.longitude <= max(p1y, p2y):
                    if point.latitude <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (point.longitude - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or point.latitude <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside


@dataclass
class VehicleTelemetry:
    """单次遥测数据点"""
    vehicle_id: str
    timestamp: datetime
    latitude: float
    longitude: float
    engine_rpm: int
    coolant_temp: float        # °C
    fuel_level: float          # %
    odometer: int
    battery_voltage: float     # V
    diagnostic_trouble_codes: List[str] = field(default_factory=list)
    speed_kmh: float = 0.0
    
    @property
    def location(self) -> GeoPoint:
        return GeoPoint(self.latitude, self.longitude)


@dataclass
class HealthScore:
    score: int                 # 0-100
    timestamp: datetime
    factors: Dict[str, str] = field(default_factory=dict)
    
    @property
    def status(self) -> str:
        if self.score >= 80:
            return "healthy"
        elif self.score >= 60:
            return "fair"
        elif self.score >= 40:
            return "poor"
        else:
            return "critical"


@dataclass
class MaintenanceWindow:
    recommended_date: datetime
    components: List[str]
    confidence: float          # 0.0 ~ 1.0
    urgency_level: str         # "low", "medium", "high", "immediate"


@dataclass
class GeoFenceAlert:
    rental_id: str
    vehicle_id: str
    violation_location: GeoPoint
    timestamp: datetime
    severity: str
    message: str = ""


class VehicleHealthMonitor:
    """
    车辆健康监测引擎
    基于实时遥测数据计算健康评分
    """
    
    # 阈值常量
    COOLANT_WARNING = 100.0    # °C
    COOLANT_CRITICAL = 110.0
    RPM_WARNING = 4500
    BATTERY_LOW = 12.0
    BATTERY_CRITICAL = 11.5
    
    def calculate_health_score(self, telemetry: VehicleTelemetry) -> HealthScore:
        score = 100
        factors = {}
        
        # 冷却液温度评分
        if telemetry.coolant_temp > self.COOLANT_CRITICAL:
            score -= 30
            factors["coolant_temp"] = f"critical ({telemetry.coolant_temp}°C)"
        elif telemetry.coolant_temp > self.COOLANT_WARNING:
            score -= 15
            factors["coolant_temp"] = f"warning ({telemetry.coolant_temp}°C)"
        
        # 发动机转速评分
        if telemetry.engine_rpm > self.RPM_WARNING:
            score -= 10
            factors["engine_rpm"] = f"high ({telemetry.engine_rpm} RPM)"
        
        # 电池电压评分
        if telemetry.battery_voltage < self.BATTERY_CRITICAL:
            score -= 20
            factors["battery"] = f"critical ({telemetry.battery_voltage}V)"
        elif telemetry.battery_voltage < self.BATTERY_LOW:
            score -= 10
            factors["battery"] = f"low ({telemetry.battery_voltage}V)"
        
        # 故障码评分（最严重）
        if telemetry.diagnostic_trouble_codes:
            dtc_penalty = min(len(telemetry.diagnostic_trouble_codes) * 15, 50)
            score -= dtc_penalty
            factors["dtc"] = f"{len(telemetry.diagnostic_trouble_codes)} codes active"
        
        # 油量评分
        if telemetry.fuel_level < 10:
            score -= 5
            factors["fuel"] = f"low ({telemetry.fuel_level}%)"
        
        final_score = max(0, score)
        return HealthScore(
            score=final_score,
            timestamp=telemetry.timestamp,
            factors=factors
        )
    
    def check_critical_alerts(self, telemetry: VehicleTelemetry) -> List[Dict]:
        """检查是否需要立即告警"""
        alerts = []
        
        if telemetry.coolant_temp > self.COOLANT_CRITICAL:
            alerts.append({
                "type": "overheating",
                "severity": AlertSeverity.CRITICAL,
                "message": f"Engine overheating: {telemetry.coolant_temp}°C"
            })
        
        if telemetry.battery_voltage < self.BATTERY_CRITICAL:
            alerts.append({
                "type": "battery_failure",
                "severity": AlertSeverity.CRITICAL,
                "message": f"Battery critical: {telemetry.battery_voltage}V"
            })
        
        if telemetry.diagnostic_trouble_codes:
            alerts.append({
                "type": "engine_fault",
                "severity": AlertSeverity.HIGH,
                "message": f"DTCs detected: {telemetry.diagnostic_trouble_codes}"
            })
        
        return alerts


class PredictiveMaintenanceEngine:
    """
    预测性维护引擎（简化实现）
    生产环境应集成 scikit-learn/TensorFlow 模型
    """
    
    def __init__(self):
        # 规则库：基于里程和时间的维护建议
        self.maintenance_rules = {
            "oil_change": {"mileage_interval": 10000, "time_interval_days": 180},
            "tire_rotation": {"mileage_interval": 8000, "time_interval_days": 365},
            "brake_inspection": {"mileage_interval": 20000, "time_interval_days": 365},
            "transmission_service": {"mileage_interval": 60000, "time_interval_days": 730},
            "coolant_flush": {"mileage_interval": 50000, "time_interval_days": 730},
        }
    
    def predict_maintenance_window(
        self,
        vehicle_id: str,
        current_mileage: int,
        last_service_mileage: Dict[str, int],
        last_service_dates: Dict[str, datetime],
        telemetry_history: List[VehicleTelemetry]
    ) -> MaintenanceWindow:
        """
        基于规则引擎预测下一次保养
        """
        upcoming_services = []
        urgency_scores = []
        
        for service_type, rules in self.maintenance_rules.items():
            last_mileage = last_service_mileage.get(service_type, 0)
            last_date = last_service_dates.get(service_type, datetime.min)
            
            miles_since = current_mileage - last_mileage
            days_since = (datetime.now() - last_date).days
            
            mileage_ratio = miles_since / rules["mileage_interval"]
            time_ratio = days_since / rules["time_interval_days"]
            
            # 取更紧迫的指标
            urgency = max(mileage_ratio, time_ratio)
            urgency_scores.append(urgency)
            
            if urgency >= 0.8:  # 接近或超过维护周期
                days_until = max(0, int((1 - urgency) * rules["time_interval_days"]))
                upcoming_services.append({
                    "type": service_type,
                    "urgency": urgency,
                    "days_until": days_until,
                    "reason": f"miles: {miles_since}/{rules['mileage_interval']} "
                              f"days: {days_since}/{rules['time_interval_days']}"
                })
        
        # 分析遥测数据增强预测
        if telemetry_history:
            recent_temps = [t.coolant_temp for t in telemetry_history[-50:]]
            avg_temp = statistics.mean(recent_temps) if recent_temps else 90
            if avg_temp > 95:
                upcoming_services.append({
                    "type": "cooling_system_check",
                    "urgency": 0.9,
                    "days_until": 7,
                    "reason": f"average coolant temp {avg_temp:.1f}°C"
                })
        
        # 排序并生成建议
        upcoming_services.sort(key=lambda x: x["urgency"], reverse=True)
        
        if not upcoming_services:
            return MaintenanceWindow(
                recommended_date=datetime.now() + timedelta(days=30),
                components=["routine_inspection"],
                confidence=0.7,
                urgency_level="low"
            )
        
        most_urgent = upcoming_services[0]
        avg_urgency = sum(urgency_scores) / len(urgency_scores) if urgency_scores else 0
        
        if avg_urgency >= 1.0:
            urgency_level = "immediate"
            days_offset = 0
        elif avg_urgency >= 0.9:
            urgency_level = "high"
            days_offset = 7
        elif avg_urgency >= 0.7:
            urgency_level = "medium"
            days_offset = 14
        else:
            urgency_level = "low"
            days_offset = 30
        
        return MaintenanceWindow(
            recommended_date=datetime.now() + timedelta(days=days_offset),
            components=[s["type"] for s in upcoming_services[:3]],
            confidence=min(0.95, 0.5 + avg_urgency * 0.5),
            urgency_level=urgency_level
        )


class GeoFenceService:
    """
    地理围栏服务
    防止车辆越界使用
    """
    
    def __init__(self):
        self._fences: Dict[str, GeoPolygon] = {}
        self._rental_vehicles: Dict[str, str] = {}  # rental_id -> vehicle_id
    
    def set_rental_boundary(self, rental_id: str, vehicle_id: str, allowed_area: GeoPolygon):
        self._fences[rental_id] = allowed_area
        self._rental_vehicles[rental_id] = vehicle_id
    
    def check_violation(self, rental_id: str, current_location: GeoPoint) -> Optional[GeoFenceAlert]:
        if rental_id not in self._fences:
            return None
        
        fence = self._fences[rental_id]
        if fence.contains(current_location):
            return None
        
        return GeoFenceAlert(
            rental_id=rental_id,
            vehicle_id=self._rental_vehicles.get(rental_id, "unknown"),
            violation_location=current_location,
            timestamp=datetime.now(),
            severity="HIGH",
            message="Vehicle has left the authorized rental area"
        )
    
    def remove_boundary(self, rental_id: str):
        self._fences.pop(rental_id, None)
        self._rental_vehicles.pop(rental_id, None)


class NotificationService:
    """
    通知服务（模拟）
    生产环境应集成 SendGrid/Amazon SES/Twilio
    """
    
    @staticmethod
    def send_alert(alert: GeoFenceAlert):
        print(f"[ALERT] GeoFence Violation!")
        print(f"  Rental: {alert.rental_id}")
        print(f"  Vehicle: {alert.vehicle_id}")
        print(f"  Location: ({alert.violation_location.latitude}, {alert.violation_location.longitude})")
        print(f"  Severity: {alert.severity}")
        print(f"  Time: {alert.timestamp}")
    
    @staticmethod
    def send_maintenance_alert(vehicle_id: str, window: MaintenanceWindow):
        print(f"[MAINTENANCE] Vehicle {vehicle_id} maintenance scheduled")
        print(f"  Date: {window.recommended_date.date()}")
        print(f"  Components: {', '.join(window.components)}")
        print(f"  Urgency: {window.urgency_level}")
        print(f"  Confidence: {window.confidence:.0%}")
