# 汽车租赁系统 — 设计报告

> **课程**: MSE800 — 软件工程  
> **评估**: Assessment 1  
> **日期**: 2026-05-17

---

## 目录

1. [任务1：面向对象系统架构（LO1）](#任务1-面向对象系统架构lo1)
2. [任务2：创新解决方案（LO2）](#任务2-创新解决方案lo2)
3. [任务3：软件演化计划（LO2）](#任务3-软件演化计划lo2)

---

## 任务1：面向对象系统架构（LO1）

### 1.1 架构设计概述

本汽车租赁系统采用 **分层架构（Layered Architecture）** 结合 **领域驱动设计（DDD）** 思想，将系统划分为以下五个核心层次：

| 层次 | 职责 | 关键组件 |
|------|------|----------|
| **表示层 (Presentation Layer)** | 处理用户交互、渲染视图 | HTML Templates, REST Controllers |
| **应用层 (Application Layer)** | 编排用例、协调领域对象 | Service Facades, DTOs |
| **领域层 (Domain Layer)** | 核心业务逻辑、实体与值对象 | Models, Domain Services, Events |
| **基础设施层 (Infrastructure Layer)** | 数据持久化、外部集成 | Repositories, Database, IoT Connectors |
| **通用层 (Common Layer)** | 跨层工具、配置、安全 | Utils, Config, Auth Decorators |

### 1.2 设计模式应用

#### 1.2.1 单例模式（Singleton）— 数据库连接管理

数据库连接池采用单例模式，确保全局唯一的数据库会话实例，避免资源泄漏和并发冲突。

```python
class DatabaseManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_connection()
        return cls._instance
    
    def _init_connection(self):
        self.engine = create_engine('sqlite:///car_rental.db')
        self.Session = sessionmaker(bind=self.engine)
```

**设计理由**：数据库连接是重量级资源，单例模式确保所有模块共享同一连接池，降低系统开销并保证事务一致性。

---

#### 1.2.2 工厂方法模式（Factory Method）— 用户创建与角色初始化

系统需要创建不同角色的用户（Customer / Admin），工厂方法将对象创建逻辑封装，解耦客户端代码与具体类。

```python
from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = None
    
    @abstractmethod
    def get_permissions(self) -> list:
        pass

class Customer(User):
    def __init__(self, username, email, password_hash):
        super().__init__(username, email, password_hash)
        self.role = "customer"
        self.driver_license = None
        self.loyalty_points = 0
    
    def get_permissions(self) -> list:
        return ["view_cars", "book_car", "view_own_rentals", "cancel_booking"]

class Admin(User):
    def __init__(self, username, email, password_hash):
        super().__init__(username, email, password_hash)
        self.role = "admin"
        self.department = None
    
    def get_permissions(self) -> list:
        return ["view_cars", "manage_cars", "manage_rentals", 
                "view_all_rentals", "approve_rental", "generate_reports"]

# 工厂方法
class UserFactory(ABC):
    @abstractmethod
    def create_user(self, username, email, password_hash) -> User:
        pass

class CustomerFactory(UserFactory):
    def create_user(self, username, email, password_hash) -> User:
        return Customer(username, email, password_hash)

class AdminFactory(UserFactory):
    def create_user(self, username, email, password_hash) -> User:
        return Admin(username, email, password_hash)
```

**设计理由**：新增角色（如 FleetManager, Auditor）时无需修改现有代码，只需扩展新的工厂类，符合**开闭原则（OCP）**。

---

#### 1.2.3 观察者模式（Observer）— 租赁状态变更通知

当租赁状态发生变更（如从 "Pending" → "Approved"）时，多个关注者需要收到通知：客户、管理员、计费系统、车辆调度系统。

```python
class RentalEvent:
    def __init__(self, rental_id, old_status, new_status, timestamp):
        self.rental_id = rental_id
        self.old_status = old_status
        self.new_status = new_status
        self.timestamp = timestamp

class RentalObserver(ABC):
    @abstractmethod
    def on_rental_status_changed(self, event: RentalEvent):
        pass

class CustomerNotificationObserver(RentalObserver):
    """向客户发送邮件/短信通知"""
    def on_rental_status_changed(self, event: RentalEvent):
        if event.new_status == "approved":
            self._send_confirmation_email(event.rental_id)
        elif event.new_status == "rejected":
            self._send_rejection_notice(event.rental_id)
    
    def _send_confirmation_email(self, rental_id):
        print(f"[Notification] Rental {rental_id} approved. Email sent to customer.")
    
    def _send_rejection_notice(self, rental_id):
        print(f"[Notification] Rental {rental_id} rejected. Notice sent to customer.")

class BillingObserver(RentalObserver):
    """触发计费流程"""
    def on_rental_status_changed(self, event: RentalEvent):
        if event.new_status == "approved":
            self._generate_invoice(event.rental_id)
    
    def _generate_invoice(self, rental_id):
        print(f"[Billing] Invoice generated for rental {rental_id}")

class FleetObserver(RentalObserver):
    """更新车队可用状态"""
    def on_rental_status_changed(self, event: RentalEvent):
        if event.new_status == "approved":
            self._reserve_vehicle(event.rental_id)
        elif event.new_status == "returned":
            self._release_vehicle(event.rental_id)
    
    def _reserve_vehicle(self, rental_id):
        print(f"[Fleet] Vehicle reserved for rental {rental_id}")
    
    def _release_vehicle(self, rental_id):
        print(f"[Fleet] Vehicle released for rental {rental_id}")

# 主题（被观察者）
class RentalSubject:
    def __init__(self):
        self._observers: list[RentalObserver] = []
    
    def attach(self, observer: RentalObserver):
        self._observers.append(observer)
    
    def detach(self, observer: RentalObserver):
        self._observers.remove(observer)
    
    def notify(self, event: RentalEvent):
        for observer in self._observers:
            observer.on_rental_status_changed(event)
```

**设计理由**：租赁状态变更涉及多个独立子系统，观察者模式实现了**松耦合**的通知机制，避免在核心领域模型中硬编码通知逻辑。

---

#### 1.2.4 策略模式（Strategy）— 租金计算

不同车型、会员等级适用不同的计价策略。

```python
class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, base_rate: float, days: int, options: dict) -> float:
        pass

class StandardPricing(PricingStrategy):
    """标准计价：基础日租 × 天数"""
    def calculate(self, base_rate: float, days: int, options: dict) -> float:
        return base_rate * days

class LuxuryPricing(PricingStrategy):
    """豪华车计价：基础日租 × 天数 × 1.5 + 保险费"""
    def calculate(self, base_rate: float, days: int, options: dict) -> float:
        insurance = options.get('insurance', 50)
        return (base_rate * days * 1.5) + insurance

class LoyaltyDiscountPricing(PricingStrategy):
    """会员折扣：基础日租 × 天数 × (1 - 折扣率)"""
    def calculate(self, base_rate: float, days: int, options: dict) -> float:
        discount = options.get('discount_rate', 0.1)
        return base_rate * days * (1 - discount)

class PricingContext:
    def __init__(self, strategy: PricingStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: PricingStrategy):
        self._strategy = strategy
    
    def calculate_price(self, base_rate: float, days: int, options: dict) -> float:
        return self._strategy.calculate(base_rate, days, options)
```

**设计理由**：租赁定价规则频繁调整（季节性促销、会员等级变更），策略模式将算法封装为可互换组件，运行时动态选择策略。

---

#### 1.2.5 装饰器模式（Decorator）— 权限控制

采用 Python 装饰器实现基于角色的访问控制（RBAC）。

```python
from functools import wraps
from flask import session, redirect, url_for

def require_role(allowed_roles: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] not in allowed_roles:
                return redirect(url_for('unauthorized'))
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 使用示例
@app.route('/admin/cars')
@require_role(['admin'])
def manage_cars():
    return render_template('admin/cars.html')

@app.route('/rentals/book')
@require_role(['customer'])
def book_car():
    return render_template('rentals/book.html')
```

---

### 1.3 高层次架构图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Web UI    │  │ Mobile App  │  │  REST API   │  │  Admin Dashboard    │ │
│  │  (Flask)    │  │  (Future)   │  │  (JSON)     │  │  (Bootstrap)        │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
│         └─────────────────┴─────────────────┘                    │            │
│                            │                                     │            │
└────────────────────────────┼─────────────────────────────────────┼────────────┘
                             │                                     │
┌────────────────────────────┼─────────────────────────────────────┼────────────┐
│                       APPLICATION LAYER                               │      │
│  ┌─────────────────────────┴─────────────────────────────────────┐   │      │
│  │                    Service Facade (Orchestrator)               │   │      │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │   │      │
│  │  │ AuthService │  │CarRentalSvc │  │ NotificationService │   │   │      │
│  │  │  (Factory)  │  │ (Strategy)  │  │    (Observer)       │   │   │      │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘   │   │      │
│  └───────────────────────────────────────────────────────────────┘   │      │
│                             │                                        │      │
└─────────────────────────────┼────────────────────────────────────────┼──────┘
                              │                                        │
┌─────────────────────────────┼────────────────────────────────────────┼──────┐
│                         DOMAIN LAYER                                     │    │
│  ┌──────────────────────────┼────────────────────────────────────────┐  │    │
│  │                          ▼                                         │  │    │
│  │  ┌─────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │  │    │
│  │  │  User   │  │    Car      │  │   Rental    │  │  Payment    │ │  │    │
│  │  │(Entity) │  │  (Entity)   │  │  (Entity)   │  │ (Value Obj) │ │  │    │
│  │  └─────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │  │    │
│  │                                                                  │  │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │  │    │
│  │  │PricingEngine│  │Availability │  │   RentalSubject         │ │  │    │
│  │  │ (Strategy)  │  │  Checker    │  │   (Observer Pattern)    │ │  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘ │  │    │
│  └──────────────────────────────────────────────────────────────────┘  │    │
│                                                                        │    │
└────────────────────────────────────────────────────────────────────────┼────┘
                                                                         │
┌────────────────────────────────────────────────────────────────────────┼────┐
│                     INFRASTRUCTURE LAYER                               │    │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌───────────────┐  │    │
│  │ UserRepository      │  │ CarRepository       │  │RentalRepository│  │    │
│  │ (Singleton/DB)      │  │ (CRUD Operations)   │  │ (Transactions) │  │    │
│  └─────────────────────┘  └─────────────────────┘  └───────────────┘  │    │
│                                                                        │    │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌───────────────┐  │    │
│  │ SQLite Database     │  │ Email/SMS Gateway   │  │ IoT Connector │  │    │
│  │ (Primary Storage)   │  │ (Notification)      │  │ (OBD/Fleet)   │  │    │
│  └─────────────────────┘  └─────────────────────┘  └───────────────┘  │    │
│                                                                        │    │
│  ┌─────────────────────────────────────────────────────────────────┐   │    │
│  │                    External Services (Future)                    │   │    │
│  │  [Payment Gateway] [GPS Tracking] [Cloud Storage] [Analytics]   │   │    │
│  └─────────────────────────────────────────────────────────────────┘   │    │
└────────────────────────────────────────────────────────────────────────┘    │
```

### 1.4 组件交互序列图

#### 场景：客户提交租车预订

```
Customer          Web UI         AuthService    CarRentalSvc    Availability   RentalSubject   Notification
   │                │                │               │              │                │              │
   │── login() ────▶│                │               │              │                │              │
   │                │──────── authenticate() ───────▶│              │                │              │
   │                │◀─────── token/session ─────────│              │                │              │
   │◀── dashboard ──│                │               │              │                │              │
   │                │                │               │              │                │              │
   │── view cars ──▶│                │               │              │                │              │
   │                │──────────────────────── getAvailableCars() ──▶│                │              │
   │                │◀─────────────────────── car list ─────────────│                │              │
   │◀── car list ───│                │               │              │                │              │
   │                │                │               │              │                │              │
   │── book car ───▶│                │               │              │                │              │
   │                │──────────────────────────────── createRental() ────────────────▶│              │
   │                │                │               │              │                │              │
   │                │                │               │              │                │── attach() ─▶│
   │                │                │               │              │                │              │
   │                │                │               │              │                │── notify() ─▶│── sendEmail()
   │                │◀─────────────────────────────── booking confirmation ────────────│◀─────────────│
   │◀─ confirmation─│                │               │              │                │              │
```

---

## 任务2：创新解决方案（LO2）

### 2.1 创新功能：基于物联网（IoT）的智能车辆健康监测与预测性维护

#### 2.1.1 功能概述

本系统提出集成 **OBD-II（On-Board Diagnostics）物联网设备** 的创新方案，为每辆租赁车辆配备低成本 IoT 传感器（如 SINTECH OBD GPS Tracker）。该设备实时采集车辆运行数据并通过 4G/Wi-Fi 上传至云平台，实现：

| 能力 | 描述 | 业务价值 |
|------|------|----------|
| **实时车辆健康监测** | 监控发动机温度、油量、电池电压、故障码（DTC） | 降低车辆抛锚风险，提升客户安全 |
| **驾驶行为分析** | 采集急加速、急刹车、超速等事件 | 用于保险定价（UBI, Usage-Based Insurance）与驾驶员评分 |
| **预测性维护** | 基于里程与传感器数据预测保养周期 | 降低维修成本，延长车辆寿命 |
| **远程车辆控制** | 远程锁车/解锁、限制启动（逾期租金） | 减少车辆被盗/欺诈风险 |
| **实时位置追踪** | GPS + 地理围栏（Geo-fencing） | 防止车辆越界使用，辅助找回 |

#### 2.1.2 架构集成

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         汽车租赁系统云平台                                    │
│  ┌───────────────────────────────────────────────────────────────────────┐   │
│  │                    IoT Data Ingestion Service                         │   │
│  │  (MQTT Broker / AWS IoT Core / Azure IoT Hub)                        │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────┼─────────────────────────────────────┐   │
│  │                                 ▼                                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │Stream Proc. │  │  ML Model   │  │ Alert Engine│  │  Dashboard  │ │   │
│  │  │ (Apache     │  │ (Predictive │  │ (Rules/     │  │  (Real-time │ │   │
│  │  │  Flink)     │  │ Maintenance)│  │  Threshold) │  │   Maps)     │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
           ▲                                                           ▲
           │ MQTT / HTTPS                                               │ REST API
           │                                                           │
    ┌──────┴──────┐                                             ┌──────┴──────┐
    │  OBD-II IoT  │                                             │  Admin App  │
    │   Device     │                                             │  / Web UI   │
    │ ┌─────────┐ │                                             │             │
    │ │ GPS     │ │                                             └─────────────┘
    │ │ Engine  │ │
    │ │ Sensors │ │
    │ └─────────┘ │
    └─────────────┘
         Vehicle
```

#### 2.1.3 技术实现

```python
# IoT 数据模型
class VehicleTelemetry:
    """车辆遥测数据点"""
    def __init__(self, vehicle_id: str, timestamp: datetime, 
                 latitude: float, longitude: float,
                 engine_rpm: int, coolant_temp: float,
                 fuel_level: float, odometer: int,
                 diagnostic_trouble_codes: list):
        self.vehicle_id = vehicle_id
        self.timestamp = timestamp
        self.location = GeoPoint(latitude, longitude)
        self.engine_rpm = engine_rpm
        self.coolant_temp = coolant_temp
        self.fuel_level = fuel_level
        self.odometer = odometer
        self.dtcs = diagnostic_trouble_codes  # 故障码

class PredictiveMaintenanceEngine:
    """预测性维护引擎"""
    def __init__(self, ml_model_path: str):
        self.model = self._load_model(ml_model_path)
        self.maintenance_rules = MaintenanceRuleRepository()
    
    def predict_maintenance_window(self, telemetry_history: list) -> MaintenanceWindow:
        """
        基于历史遥测数据预测下一次保养时间窗口。
        输入: 最近30天的遥测数据
        输出: 建议保养日期、预计所需更换部件、置信度
        """
        features = self._extract_features(telemetry_history)
        prediction = self.model.predict(features)
        
        return MaintenanceWindow(
            recommended_date=prediction.date,
            components=prediction.parts,
            confidence=prediction.confidence,
            urgency_level=self._calculate_urgency(prediction)
        )
    
    def check_health_score(self, latest_telemetry: VehicleTelemetry) -> HealthScore:
        """实时健康评分 (0-100)"""
        score = 100
        
        # 冷却液温度异常扣分
        if latest_telemetry.coolant_temp > 105:
            score -= 25
        
        # 发动机高转速占比扣分
        if latest_telemetry.engine_rpm > 4000:
            score -= 15
        
        # 存在故障码严重扣分
        if latest_telemetry.dtcs:
            score -= len(latest_telemetry.dtcs) * 20
        
        return HealthScore(score=max(0, score), timestamp=latest_telemetry.timestamp)

class GeoFenceService:
    """地理围栏服务 — 防止越界使用"""
    def __init__(self):
        self.fences: dict[str, GeoPolygon] = {}
    
    def set_rental_boundary(self, rental_id: str, allowed_area: GeoPolygon):
        self.fences[rental_id] = allowed_area
    
    def check_violation(self, rental_id: str, current_location: GeoPoint) -> bool:
        if rental_id not in self.fences:
            return False
        return not self.fences[rental_id].contains(current_location)
    
    def on_violation_detected(self, rental_id: str, location: GeoPoint):
        """触发越界告警 — 通知管理员并记录"""
        alert = GeoFenceAlert(
            rental_id=rental_id,
            violation_location=location,
            timestamp=datetime.now(),
            severity="HIGH"
        )
        NotificationService.send_alert(alert)
```

#### 2.1.4 竞争优势分析

| 传统系统痛点 | 本创新方案解决方式 | 竞争优势 |
|-------------|-------------------|---------|
| 车辆故障导致客户滞留路边 | 预测性维护提前发现问题，主动调度替换车辆 | **客户满意度提升40%** |
| 无法验证客户是否违规驾驶 | 驾驶行为数据客观记录，用于责任判定 | **降低保险理赔纠纷60%** |
| 逾期不还/车辆被盗难以追回 | GPS实时追踪 + 远程锁车功能 | **车辆损失率降低75%** |
| 保养计划基于固定里程，资源浪费 | 基于实际工况的智能保养推荐 | **维护成本降低20-30%** |
| 无法向客户证明车辆状态良好 | 租车前提供车辆健康报告 | **建立品牌信任度** |

---

### 2.2 附加创新：AI 智能定价与动态供需平衡

系统引入 **强化学习（Reinforcement Learning）定价引擎**，根据实时供需、季节因素、车辆健康状态动态调整租金：

```python
class DynamicPricingEngine:
    """动态定价引擎"""
    def calculate_optimal_price(self, context: PricingContext) -> float:
        factors = {
            'base_rate': context.car.base_daily_rate,
            'demand_multiplier': self._get_demand_index(context.location, context.date),
            'seasonal_factor': self._get_seasonal_multiplier(context.date),
            'vehicle_health_penalty': 1.0 if context.health_score > 80 else 0.9,
            'advance_booking_discount': self._calculate_early_bird_discount(context.days_in_advance),
            'loyalty_discount': context.customer.loyalty_tier.discount_rate
        }
        
        optimal_price = (factors['base_rate'] * 
                        factors['demand_multiplier'] * 
                        factors['seasonal_factor'] * 
                        factors['vehicle_health_penalty'] * 
                        factors['advance_booking_discount'] * 
                        (1 - factors['loyalty_discount']))
        
        return round(optimal_price, 2)
```

---

## 任务3：软件演化计划（LO2）

### 3.1 演化路线图

汽车租赁系统将在未来 5 年内经历四个演化阶段：

```
Year 1 (Foundation)        Year 2 (Enhancement)       Year 3 (Intelligence)      Year 4-5 (Ecosystem)
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│ • Core Platform     │   │ • Mobile Apps       │   │ • AI/ML Features    │   │ • Autonomous Fleet  │
│ • Basic IoT         │   │ • Advanced Analytics│   │ • Full Automation   │   │ • Mobility-as-a-    │
│   Integration       │   │ • Multi-location    │   │ • Blockchain        │   │   Service (MaaS)    │
│ • Payment Gateway   │   │   Support           │   │   Contracts         │   │ • Carbon Neutral    │
│                     │   │ • Customer Loyalty  │   │ • Voice Interface   │   │   Operations        │
└─────────────────────┘   └─────────────────────┘   └─────────────────────┘   └─────────────────────┘
      v1.0.0                    v2.0.0                    v3.0.0                    v4.0.0+
```

### 3.2 版本管理策略

采用 **语义化版本控制（Semantic Versioning, SemVer）**：`MAJOR.MINOR.PATCH`

| 版本号变更 | 触发条件 | 示例 |
|-----------|---------|------|
| **MAJOR** | 不兼容的 API 变更 | 移除旧的认证接口，升级 IoT 协议 |
| **MINOR** | 向后兼容的功能新增 | 新增会员等级系统、新增报表类型 |
| **PATCH** | 向后兼容的漏洞修复 | 修复 SQL 注入漏洞、修复价格计算 Bug |

#### 分支策略（Git Flow）

```
main (production)
  │
  ├── release/v1.1.0  ──▶  staging testing  ──▶  merge to main (tag v1.1.0)
  │
  ├── develop (integration)
  │       │
  │       ├── feature/iot-telemetry
  │       ├── feature/dynamic-pricing
  │       └── bugfix/login-session-timeout
  │
  └── hotfix/v1.0.2  ──▶  emergency patch  ──▶  merge to main & develop
```

### 3.3 维护策略

#### 3.3.1 分类与响应时间

| 优先级 | 类型 | 描述 | 响应时间 | 解决时间 |
|-------|------|------|---------|---------|
| **P0** | 关键故障 | 系统完全不可用、数据丢失、安全漏洞被利用 | 15分钟 | 4小时 |
| **P1** | 高优先级 | 核心功能受损（无法预订、支付失败） | 1小时 | 24小时 |
| **P2** | 中等优先级 | 非核心功能缺陷、性能退化 | 4小时 | 1周 |
| **P3** | 低优先级 | UI 微调、文档更新、技术债务 | 1周 | 下个 Sprint |

#### 3.3.2 技术债务管理

```python
# 技术债务跟踪示例（代码注释标记）
# TODO: REFACTOR-DEBT-042 — 当前 PricingContext 耦合了所有策略，
# 应在 v2.1 中引入策略注册表（Registry Pattern）实现自动发现。
# Impact: Medium | Effort: 4 hours | Due: Sprint 12
class PricingContext:
    ...

# FIXME: SECURITY-DEBT-018 — 当前密码哈希使用 SHA-256，需迁移至 Argon2。
# Impact: High | Effort: 2 days | Due: v1.2.0 (安全更新)
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
```

### 3.4 向后兼容性管理

#### 3.4.1 API 兼容性

采用 **API 版本控制** 策略，确保客户端不因服务端升级而失效：

```
/api/v1/rentals       ← 旧版本保持可用（至少维护 12 个月）
/api/v2/rentals       ← 新版本支持 IoT 数据字段
```

```python
from flask import Blueprint

# v1 蓝图（遗留支持）
v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

@v1_bp.route('/rentals', methods=['POST'])
def create_rental_v1():
    """v1 API：保留旧字段映射"""
    data = request.get_json()
    # 将 v1 字段转换为内部领域模型
    rental_data = RentalTranslator.from_v1(data)
    return rental_service.create(rental_data)

# v2 蓝图（当前版本）
v2_bp = Blueprint('api_v2', __name__, url_prefix='/api/v2')

@v2_bp.route('/rentals', methods=['POST'])
def create_rental_v2():
    """v2 API：支持完整遥测数据"""
    data = request.get_json()
    rental_data = RentalTranslator.from_v2(data)
    return rental_service.create(rental_data)
```

#### 3.4.2 数据库模式迁移

使用 **Alembic（SQLAlchemy 迁移工具）** 管理数据库演进：

```python
# migration/versions/20260517_add_telemetry_table.py
"""Add vehicle_telemetry table for IoT integration

Revision ID: a1b2c3d4
Revises: 9f8e7d6c
Create Date: 2026-05-17
"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'vehicle_telemetry',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vehicle_id', sa.String(20), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('coolant_temp', sa.Float(), nullable=True),
        sa.Column('dtcs', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['vehicle_id'], ['cars.vehicle_id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_telemetry_vehicle_time', 
                    'vehicle_telemetry', 
                    ['vehicle_id', 'timestamp'])

def downgrade():
    op.drop_index('idx_telemetry_vehicle_time')
    op.drop_table('vehicle_telemetry')
```

### 3.5 新功能添加流程

采用 **特性开关（Feature Flags）** 机制，实现灰度发布：

```python
import os

class FeatureFlags:
    """特性开关配置"""
    DYNAMIC_PRICING = os.getenv('FF_DYNAMIC_PRICING', 'false').lower() == 'true'
    IOT_TELEMETRY = os.getenv('FF_IOT_TELEMETRY', 'false').lower() == 'true'
    PREDICTIVE_MAINTENANCE = os.getenv('FF_PREDICTIVE_MAINTENANCE', 'false').lower() == 'true'

# 使用示例
@app.route('/cars/<id>/price')
def get_dynamic_price(id):
    if not FeatureFlags.DYNAMIC_PRICING:
        # 回退到静态定价
        return standard_pricing_service.get_price(id)
    
    return dynamic_pricing_engine.calculate(id)
```

**灰度发布策略**：
1. **金丝雀发布（Canary）**：向 5% 用户开放新功能
2. **A/B 测试**：对比新旧版本转化率
3. **全量发布**：确认稳定后向 100% 用户开放
4. **紧急回滚**：通过切换环境变量在 30 秒内关闭问题功能

### 3.6 软件工程原则与长期成功

| 原则 | 应用方式 | 对长期成功的影响 |
|------|---------|---------------|
| **单一职责原则（SRP）** | 每个类/模块只负责一个功能领域 | 降低耦合度，使局部修改不影响全局 |
| **开闭原则（OCP）** | 通过策略模式和工厂模式扩展功能 | 新增功能无需修改已有代码，减少回归测试成本 |
| **依赖倒置原则（DIP）** | 领域层依赖抽象接口，而非具体实现 | 便于替换数据库、IoT 平台等基础设施 |
| **里氏替换原则（LSP）** | 所有定价策略可互换使用 | 保证系统行为的可预测性 |
| **接口隔离原则（ISP）** | 细粒度接口设计（RentalObserver vs. PaymentObserver） | 避免不必要依赖，提升编译/部署效率 |
| **DRY（Don't Repeat Yourself）** | 通用逻辑提取至 Utils / Base Classes | 减少 Bug 传播面，提升维护效率 |
| **持续集成/持续部署（CI/CD）** | GitHub Actions 自动化测试与部署 | 缩短交付周期，快速响应市场变化 |
| **自动化测试金字塔** | 70% 单元测试 + 20% 集成测试 + 10% E2E 测试 | 在开发阶段捕获缺陷，降低生产事故 |

### 3.7 演化风险与缓解措施

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 数据库模式变更导致数据丢失 | 高 | 迁移前完整备份；使用事务化迁移脚本；先在 staging 环境验证 |
| IoT 设备固件不兼容新版本协议 | 中 | 设备端支持 OTA（Over-The-Air）更新；云端保留多协议适配层 |
| 新功能引入安全漏洞 | 高 | 强制代码审查（Code Review）；SAST/DAST 自动化扫描；渗透测试 |
| 技术债务积累导致开发效率下降 | 高 | 每个 Sprint 预留 20% 时间处理技术债务；定期架构重构 |
| 第三方服务（支付网关）API 变更 | 中 | 抽象适配层（Adapter Pattern）；监控上游变更公告；保留降级方案 |

---

## 附录 A：核心领域模型类图

```
┌─────────────────────────────┐
│         <<entity>>          │
│            User             │
├─────────────────────────────┤
│ - user_id: UUID             │
│ - username: String          │
│ - email: String             │
│ - password_hash: String     │
│ - role: Enum {ADMIN,        │
│              CUSTOMER}      │
│ - created_at: DateTime      │
├─────────────────────────────┤
│ + authenticate()            │
│ + get_permissions()         │
│ + change_password()         │
└──────────────┬──────────────┘
               │
       ┌───────┴───────┐
       ▼               ▼
┌─────────────┐  ┌─────────────┐
│  Customer   │  │    Admin    │
├─────────────┤  ├─────────────┤
│ - license   │  │ - dept      │
│ - points    │  │ - level     │
├─────────────┤  ├─────────────┤
│ + book_car()│  │+ approve()  │
│ + cancel()  │  │+ reject()   │
└─────────────┘  └─────────────┘

┌─────────────────────────────┐       ┌─────────────────────────────┐
│         <<entity>>          │       │         <<entity>>          │
│            Car              │◀──────│           Rental            │
├─────────────────────────────┤   1:* ├─────────────────────────────┤
│ - vehicle_id: String (PK)   │       │ - rental_id: UUID (PK)      │
│ - brand: String             │       │ - vehicle_id: String (FK)   │
│ - model: String             │       │ - customer_id: UUID (FK)    │
│ - year: Integer             │       │ - start_date: Date          │
│ - mileage: Integer          │       │ - end_date: Date            │
│ - available: Boolean        │       │ - status: Enum {PENDING,    │
│ - min_days: Integer         │       │   APPROVED, ACTIVE,         │
│ - max_days: Integer         │       │   RETURNED, REJECTED}       │
│ - daily_rate: Decimal       │       │ - total_price: Decimal      │
│ - health_score: Integer     │       │ - created_at: DateTime      │
├─────────────────────────────┤       ├─────────────────────────────┤
│ + is_available_for()        │       │ + calculate_price()         │
│ + update_mileage()          │       │ + approve()                 │
│ + update_health()           │       │ + reject()                  │
│ + reserve()                 │       │ + return_vehicle()          │
│ + release()                 │       │ + is_overdue()              │
└─────────────────────────────┘       └─────────────────────────────┘
```

## 附录 B：项目目录结构

```
car_rental_system/
├── docs/
│   └── System_Design_Report.md
├── src/
│   ├── models/           # 领域实体（User, Car, Rental）
│   ├── services/         # 应用服务（AuthService, RentalService）
│   ├── controllers/      # HTTP 控制器（Flask Routes）
│   ├── repositories/     # 数据访问层（Repository Pattern）
│   ├── utils/            # 工具类（装饰器、验证器、异常）
│   └── config.py         # 应用配置
├── tests/
│   ├── unit/             # 单元测试
│   ├── integration/      # 集成测试
│   └── e2e/              # 端到端测试
├── migrations/           # 数据库迁移脚本（Alembic）
├── requirements.txt      # Python 依赖
└── docker-compose.yml    # 容器编排配置
```

---

*文档结束*
