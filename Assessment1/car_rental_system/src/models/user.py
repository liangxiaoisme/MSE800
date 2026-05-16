"""
用户领域模型 — 应用工厂方法模式创建不同角色用户
符合开闭原则：新增角色只需扩展新的工厂类
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List
import uuid


class Role(Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    FLEET_MANAGER = "fleet_manager"  # 为未来扩展预留


class User(ABC):
    """用户抽象基类 — 定义所有用户的通用接口"""
    
    def __init__(self, username: str, email: str, password_hash: str):
        self.user_id = uuid.uuid4()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role: Role = None
        self.created_at = datetime.now()
        self.is_active = True
    
    @abstractmethod
    def get_permissions(self) -> List[str]:
        """返回该角色拥有的权限列表"""
        pass
    
    @abstractmethod
    def get_dashboard_url(self) -> str:
        """返回该角色的默认主页"""
        pass
    
    def to_dict(self) -> dict:
        return {
            "user_id": str(self.user_id),
            "username": self.username,
            "email": self.email,
            "role": self.role.value if self.role else None,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active
        }


class Customer(User):
    """客户角色 — 可浏览车辆、提交预订、管理自己的订单"""
    
    def __init__(self, username: str, email: str, password_hash: str):
        super().__init__(username, email, password_hash)
        self.role = Role.CUSTOMER
        self.driver_license = None
        self.loyalty_points = 0
        self.loyalty_tier = "bronze"  # bronze, silver, gold, platinum
        self.rental_history = []
    
    def get_permissions(self) -> List[str]:
        return [
            "view_cars",
            "view_car_details",
            "book_car",
            "view_own_rentals",
            "cancel_pending_rental",
            "update_profile",
            "submit_feedback"
        ]
    
    def get_dashboard_url(self) -> str:
        return "/customer/dashboard"
    
    def add_loyalty_points(self, points: int):
        """根据消费增加积分并自动升级会员等级"""
        self.loyalty_points += points
        self._update_tier()
    
    def _update_tier(self):
        if self.loyalty_points >= 5000:
            self.loyalty_tier = "platinum"
        elif self.loyalty_points >= 2000:
            self.loyalty_tier = "gold"
        elif self.loyalty_points >= 500:
            self.loyalty_tier = "silver"
    
    def get_discount_rate(self) -> float:
        """根据会员等级返回折扣率"""
        tiers = {"bronze": 0.0, "silver": 0.05, "gold": 0.10, "platinum": 0.15}
        return tiers.get(self.loyalty_tier, 0.0)


class Admin(User):
    """管理员角色 — 拥有系统的全部管理权限"""
    
    def __init__(self, username: str, email: str, password_hash: str):
        super().__init__(username, email, password_hash)
        self.role = Role.ADMIN
        self.department = "operations"
        self.access_level = 1  # 1=standard, 2=super
    
    def get_permissions(self) -> List[str]:
        return [
            "view_cars",
            "manage_cars",          # 添加、修改、删除车辆
            "view_all_rentals",
            "approve_rental",
            "reject_rental",
            "manage_users",
            "view_reports",
            "export_data",
            "system_configuration"
        ]
    
    def get_dashboard_url(self) -> str:
        return "/admin/dashboard"


# ═══════════════════════════════════════════════════════════
# 工厂方法模式 — 用户创建工厂
# ═══════════════════════════════════════════════════════════

class UserFactory(ABC):
    """用户工厂抽象基类"""
    
    @abstractmethod
    def create_user(self, username: str, email: str, password_hash: str) -> User:
        pass


class CustomerFactory(UserFactory):
    """客户工厂"""
    
    def create_user(self, username: str, email: str, password_hash: str) -> Customer:
        return Customer(username, email, password_hash)


class AdminFactory(UserFactory):
    """管理员工厂"""
    
    def create_user(self, username: str, email: str, password_hash: str) -> Admin:
        return Admin(username, email, password_hash)


class UserFactoryRegistry:
    """
    工厂注册表 — 支持运行时注册新的用户类型工厂
    符合开闭原则：新增角色无需修改此类的现有代码
    """
    
    _factories: dict = {}
    
    @classmethod
    def register(cls, role: Role, factory: UserFactory):
        cls._factories[role] = factory
    
    @classmethod
    def get_factory(cls, role: Role) -> UserFactory:
        factory = cls._factories.get(role)
        if not factory:
            raise ValueError(f"未注册的角色类型: {role}")
        return factory
    
    @classmethod
    def create_user(cls, role: Role, username: str, email: str, password_hash: str) -> User:
        factory = cls.get_factory(role)
        return factory.create_user(username, email, password_hash)


# 初始化默认工厂注册
UserFactoryRegistry.register(Role.CUSTOMER, CustomerFactory())
UserFactoryRegistry.register(Role.ADMIN, AdminFactory())
