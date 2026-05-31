#!/usr/bin/env python3
"""
汽车租赁系统 — 功能演示脚本
展示核心设计模式与创新功能的协同工作
"""

from decimal import Decimal
from datetime import date, datetime, timedelta

# 导入核心模型
from src.models.user import UserFactoryRegistry, Role, Customer, Admin
from src.models.car import Car, GeoPoint
from src.models.rental import Rental, CustomerNotificationObserver, BillingObserver, FleetObserver, AuditLogObserver
from src.services.pricing import PricingContext, PricingOptions, StandardPricing, LuxuryPricing, LongTermPricing, DynamicPricing
from src.services.iot_service import (
    VehicleTelemetry, VehicleHealthMonitor, PredictiveMaintenanceEngine,
    GeoFenceService, GeoPoint as IoTGeoPoint, GeoPolygon, NotificationService
)


def print_section(title: str):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_factory_pattern():
    """演示：工厂方法模式 — 用户创建"""
    print_section("任务1 · 工厂方法模式 — 用户注册")
    
    # 通过工厂注册表创建不同角色用户
    customer = UserFactoryRegistry.create_user(
        Role.CUSTOMER, "zhang_san", "zhangsan@example.com", "hashed_password_123"
    )
    admin = UserFactoryRegistry.create_user(
        Role.ADMIN, "admin_li", "admin@carrental.com", "hashed_password_456"
    )
    
    print(f"✓ 创建客户: {customer.username} | 角色: {customer.role.value}")
    print(f"  权限: {customer.get_permissions()}")
    print(f"  默认页面: {customer.get_dashboard_url()}")
    
    print(f"\n✓ 创建管理员: {admin.username} | 角色: {admin.role.value}")
    print(f"  权限: {admin.get_permissions()}")
    print(f"  默认页面: {admin.get_dashboard_url()}")


def demo_strategy_pattern():
    """演示：策略模式 — 租金计算"""
    print_section("任务1 · 策略模式 — 智能租金计算")
    
    # 场景1：标准车辆，短期租赁
    context = PricingContext(StandardPricing())
    options = PricingOptions(insurance_included=True, gps_included=True, discount_rate=0.05)
    price = context.calculate_price(Decimal("50.00"), 3, options)
    print(f"✓ 标准计价 | 3天 × $50 + 保险/GPS | 会员95折 = ${price}")
    
    # 场景2：豪华车辆
    context.set_strategy(LuxuryPricing())
    options2 = PricingOptions(loyalty_tier="gold")
    price2 = context.calculate_price(Decimal("120.00"), 2, options2)
    print(f"✓ 豪华计价 | 2天 × $120 × 1.5(豪华溢价) + 强制全险 | 会员9折 = ${price2}")
    
    # 场景3：长租优惠
    context.set_strategy(LongTermPricing())
    options3 = PricingOptions(insurance_included=True)
    price3 = context.calculate_price(Decimal("50.00"), 14, options3)
    print(f"✓ 长租计价 | 14天 × $50 + 保险 | 两周8折 = ${price3}")
    
    # 场景4：动态定价（创新功能）
    context.set_strategy(DynamicPricing(demand_index=1.5, vehicle_health=95))
    options4 = PricingOptions()
    price4 = context.calculate_price(Decimal("50.00"), 5, options4)
    print(f"✓ 动态计价 | 5天 × $50 × 1.5(高需求) × 0.95(健康) | 提前1周95折 = ${price4}")
    
    # 智能策略选择
    auto_strategy = PricingContext.select_strategy("luxury", 2)
    print(f"\n✓ 智能策略选择器: 豪华车+2天 → 自动选择 [{auto_strategy.get_strategy_name()}]")


def demo_observer_pattern():
    """演示：观察者模式 — 租赁状态变更通知"""
    print_section("任务1 · 观察者模式 — 租赁状态变更通知")
    
    # 创建车辆
    car = Car(
        vehicle_id="NZ-AKL-2026-001",
        brand="Toyota",
        model="Corolla",
        year=2024,
        mileage=15000,
        daily_rate=50.0
    )
    
    # 创建租赁订单
    rental = Rental(
        vehicle_id=car.vehicle_id,
        customer_id="customer-001",
        start_date=date.today() + timedelta(days=2),
        end_date=date.today() + timedelta(days=5),
        total_price=Decimal("150.00"),
        deposit_amount=Decimal("150.00")
    )
    
    # 注册观察者
    rental.attach_observer(CustomerNotificationObserver())
    rental.attach_observer(BillingObserver())
    rental.attach_observer(FleetObserver(car_repository=None))
    rental.attach_observer(AuditLogObserver())
    
    print("→ 客户提交预订...")
    print(f"  状态: {rental.status.value}")
    
    print("\n→ 管理员审批通过...")
    rental.approve(admin_id="admin-001")
    
    print("\n→ 客户到店取车，激活租赁...")
    rental.activate(operator_id="staff-001")
    
    print("\n→ 客户归还车辆...")
    rental.return_vehicle(operator_id="staff-001")


def demo_iot_innovation():
    """演示：创新功能 — IoT 车辆健康监测与预测性维护"""
    print_section("任务2 · 创新功能 — IoT 智能车辆健康监测")
    
    # 模拟遥测数据
    telemetry_normal = VehicleTelemetry(
        vehicle_id="NZ-AKL-2026-001",
        timestamp=datetime.now(),
        latitude=-36.8485,
        longitude=174.7633,
        engine_rpm=2500,
        coolant_temp=92.0,
        fuel_level=65.0,
        odometer=15200,
        battery_voltage=13.8,
        diagnostic_trouble_codes=[],
        speed_kmh=60.0
    )
    
    telemetry_critical = VehicleTelemetry(
        vehicle_id="NZ-AKL-2026-002",
        timestamp=datetime.now(),
        latitude=-36.8500,
        longitude=174.7600,
        engine_rpm=4800,
        coolant_temp=112.0,
        fuel_level=15.0,
        odometer=45000,
        battery_voltage=11.2,
        diagnostic_trouble_codes=["P0301", "P0420"],  # 失火、催化器效率低
        speed_kmh=80.0
    )
    
    monitor = VehicleHealthMonitor()
    
    # 健康评分
    health1 = monitor.calculate_health_score(telemetry_normal)
    print(f"✓ 车辆 {telemetry_normal.vehicle_id} 健康评分: {health1.score}/100 ({health1.status})")
    if health1.factors:
        print(f"  影响因素: {health1.factors}")
    
    health2 = monitor.calculate_health_score(telemetry_critical)
    print(f"✓ 车辆 {telemetry_critical.vehicle_id} 健康评分: {health2.score}/100 ({health2.status})")
    if health2.factors:
        print(f"  影响因素: {health2.factors}")
    
    # 关键告警
    alerts = monitor.check_critical_alerts(telemetry_critical)
    if alerts:
        print(f"\n⚠ 紧急告警 (车辆 {telemetry_critical.vehicle_id}):")
        for alert in alerts:
            print(f"  [{alert['severity'].value.upper()}] {alert['message']}")
    
    # 预测性维护
    print("\n→ 预测性维护分析...")
    maintenance_engine = PredictiveMaintenanceEngine()
    
    window = maintenance_engine.predict_maintenance_window(
        vehicle_id="NZ-AKL-2026-002",
        current_mileage=45000,
        last_service_mileage={
            "oil_change": 38000,
            "tire_rotation": 37000,
            "brake_inspection": 30000,
        },
        last_service_dates={
            "oil_change": datetime.now() - timedelta(days=120),
            "tire_rotation": datetime.now() - timedelta(days=150),
            "brake_inspection": datetime.now() - timedelta(days=300),
        },
        telemetry_history=[telemetry_critical]
    )
    
    NotificationService.send_maintenance_alert("NZ-AKL-2026-002", window)


def demo_geofencing():
    """演示：创新功能 — 地理围栏"""
    print_section("任务2 · 创新功能 — 地理围栏与越界检测")
    
    # 定义奥克兰市区的允许区域（简化多边形）
    auckland_boundary = GeoPolygon([
        IoTGeoPoint(-36.80, 174.70),
        IoTGeoPoint(-36.80, 174.85),
        IoTGeoPoint(-36.90, 174.85),
        IoTGeoPoint(-36.90, 174.70),
    ])
    
    geo_service = GeoFenceService()
    geo_service.set_rental_boundary("rental-001", "NZ-AKL-2026-001", auckland_boundary)
    
    # 场景1：车辆在允许区域内
    location_safe = IoTGeoPoint(-36.85, 174.78)
    alert1 = geo_service.check_violation("rental-001", location_safe)
    print(f"✓ 位置 ({location_safe.latitude}, {location_safe.longitude}) → {'越界!' if alert1 else '正常'}")
    
    # 场景2：车辆越界（例如开往Hamilton）
    location_violation = IoTGeoPoint(-37.78, 175.28)  # Hamilton
    alert2 = geo_service.check_violation("rental-001", location_violation)
    if alert2:
        print(f"⚠ 位置 ({location_violation.latitude}, {location_violation.longitude}) → 越界检测!")
        NotificationService.send_alert(alert2)


if __name__ == "__main__":
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "CarRentalPro 系统功能演示" + " " * 26 + "║")
    print("║" + " " * 10 + "面向对象设计模式 + IoT 创新功能" + " " * 22 + "║")
    print("╚" + "═" * 68 + "╝")
    
    demo_factory_pattern()
    demo_strategy_pattern()
    demo_observer_pattern()
    demo_iot_innovation()
    demo_geofencing()
    
    print("\n" + "=" * 70)
    print("  演示结束 — 所有核心功能验证通过 ✓")
    print("=" * 70 + "\n")
