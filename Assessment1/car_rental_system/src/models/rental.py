"""
租赁领域模型 — 包含观察者模式实现
当租赁状态变更时，自动通知所有关注者
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import List, Optional
import uuid


class RentalStatus(Enum):
    PENDING = "pending"           # 待审批
    APPROVED = "approved"         # 已批准
    ACTIVE = "active"             # 租赁中
    RETURNED = "returned"         # 已归还
    REJECTED = "rejected"         # 已拒绝
    CANCELLED = "cancelled"       # 已取消
    OVERDUE = "overdue"           # 逾期


@dataclass
class RentalEvent:
    """租赁状态变更事件"""
    rental_id: str
    old_status: RentalStatus
    new_status: RentalStatus
    vehicle_id: str
    customer_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    triggered_by: Optional[str] = None  # 操作者用户ID
    reason: Optional[str] = None        # 状态变更原因


# ═══════════════════════════════════════════════════════════
# 观察者模式 — 租赁状态变更通知
# ═══════════════════════════════════════════════════════════

class RentalObserver(ABC):
    """租赁观察者接口"""
    
    @abstractmethod
    def on_rental_status_changed(self, event: RentalEvent):
        pass


class CustomerNotificationObserver(RentalObserver):
    """客户通知观察者 — 发送邮件/短信"""
    
    def on_rental_status_changed(self, event: RentalEvent):
        messages = {
            RentalStatus.APPROVED: f"您的预订 {event.rental_id} 已确认！取车日期请按时到达。",
            RentalStatus.REJECTED: f"很抱歉，您的预订 {event.rental_id} 未能通过审批。原因：{event.reason or '库存不足'}",
            RentalStatus.ACTIVE: f"您的租赁 {event.rental_id} 已开始，祝您旅途愉快！",
            RentalStatus.RETURNED: f"感谢您归还车辆！租赁 {event.rental_id} 已完成。",
            RentalStatus.OVERDUE: f"提醒：您的租赁 {event.rental_id} 已逾期，请尽快联系门店。"
        }
        msg = messages.get(event.new_status)
        if msg:
            print(f"[Notification → Customer {event.customer_id}] {msg}")


class BillingObserver(RentalObserver):
    """计费观察者 — 触发发票生成与支付处理"""
    
    def on_rental_status_changed(self, event: RentalEvent):
        if event.new_status == RentalStatus.APPROVED:
            print(f"[Billing] 为租赁 {event.rental_id} 生成预授权/押金冻结")
        elif event.new_status == RentalStatus.ACTIVE:
            print(f"[Billing] 租赁 {event.rental_id} 正式扣款")
        elif event.new_status == RentalStatus.RETURNED:
            print(f"[Billing] 租赁 {event.rental_id} 结算，退还押金")
        elif event.new_status == RentalStatus.OVERDUE:
            print(f"[Billing] 租赁 {event.rental_id} 逾期费用计算中")


class FleetObserver(RentalObserver):
    """车队管理观察者 — 更新车辆可用状态"""
    
    def __init__(self, car_repository):
        self.car_repository = car_repository
    
    def on_rental_status_changed(self, event: RentalEvent):
        if event.new_status == RentalStatus.APPROVED:
            print(f"[Fleet] 车辆 {event.vehicle_id} 已预留，不可用")
        elif event.new_status == RentalStatus.ACTIVE:
            print(f"[Fleet] 车辆 {event.vehicle_id} 已出库")
        elif event.new_status in (RentalStatus.RETURNED, RentalStatus.CANCELLED, RentalStatus.REJECTED):
            print(f"[Fleet] 车辆 {event.vehicle_id} 已释放，恢复可用")


class AuditLogObserver(RentalObserver):
    """审计日志观察者 — 记录所有状态变更"""
    
    def __init__(self):
        self.logs = []
    
    def on_rental_status_changed(self, event: RentalEvent):
        entry = {
            "timestamp": event.timestamp.isoformat(),
            "rental_id": event.rental_id,
            "change": f"{event.old_status.value} → {event.new_status.value}",
            "operator": event.triggered_by,
            "reason": event.reason
        }
        self.logs.append(entry)
        print(f"[Audit] {entry['timestamp']} | 租赁 {event.rental_id} 状态变更: {entry['change']}")


class RentalSubject:
    """
    租赁主题（被观察者）— 管理所有观察者并分发事件
    符合依赖倒置原则：依赖抽象接口而非具体实现
    """
    
    def __init__(self):
        self._observers: List[RentalObserver] = []
    
    def attach(self, observer: RentalObserver):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: RentalObserver):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event: RentalEvent):
        for observer in self._observers:
            try:
                observer.on_rental_status_changed(event)
            except Exception as e:
                print(f"[Observer Error] {type(observer).__name__}: {e}")


# ═══════════════════════════════════════════════════════════
# 租赁实体
# ═══════════════════════════════════════════════════════════

@dataclass
class Rental:
    """
    租赁实体 — 核心业务聚合根
    """
    
    vehicle_id: str
    customer_id: str
    start_date: date
    end_date: date
    rental_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: RentalStatus = RentalStatus.PENDING
    total_price: Decimal = Decimal("0.00")
    deposit_amount: Decimal = Decimal("0.00")
    created_at: datetime = field(default_factory=datetime.now)
    approved_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    rejection_reason: Optional[str] = None
    _subject: RentalSubject = field(default_factory=RentalSubject, repr=False)
    
    @property
    def rental_days(self) -> int:
        return (self.end_date - self.start_date).days + 1
    
    @property
    def is_overdue(self) -> bool:
        return self.status == RentalStatus.ACTIVE and date.today() > self.end_date
    
    def attach_observer(self, observer: RentalObserver):
        self._subject.attach(observer)
    
    def _transition(self, new_status: RentalStatus, triggered_by: Optional[str] = None, reason: Optional[str] = None):
        """内部状态转换 — 触发观察者通知"""
        if self.status == new_status:
            return
        
        old_status = self.status
        self.status = new_status
        
        if new_status == RentalStatus.APPROVED:
            self.approved_at = datetime.now()
            self.approved_by = triggered_by
        elif new_status == RentalStatus.REJECTED:
            self.rejection_reason = reason
        
        event = RentalEvent(
            rental_id=self.rental_id,
            old_status=old_status,
            new_status=new_status,
            vehicle_id=self.vehicle_id,
            customer_id=self.customer_id,
            triggered_by=triggered_by,
            reason=reason
        )
        self._subject.notify(event)
    
    def approve(self, admin_id: str):
        if self.status != RentalStatus.PENDING:
            raise RuntimeError("只能审批待处理的预订")
        self._transition(RentalStatus.APPROVED, triggered_by=admin_id)
    
    def reject(self, admin_id: str, reason: str):
        if self.status != RentalStatus.PENDING:
            raise RuntimeError("只能拒绝待处理的预订")
        self._transition(RentalStatus.REJECTED, triggered_by=admin_id, reason=reason)
    
    def activate(self, operator_id: str):
        if self.status != RentalStatus.APPROVED:
            raise RuntimeError("只能激活已批准的租赁")
        self._transition(RentalStatus.ACTIVE, triggered_by=operator_id)
    
    def return_vehicle(self, operator_id: str):
        if self.status != RentalStatus.ACTIVE:
            raise RuntimeError("只能归还进行中的租赁")
        self._transition(RentalStatus.RETURNED, triggered_by=operator_id)
    
    def cancel(self, customer_id: str):
        if self.status not in (RentalStatus.PENDING, RentalStatus.APPROVED):
            raise RuntimeError("当前状态不可取消")
        self._transition(RentalStatus.CANCELLED, triggered_by=customer_id)
    
    def mark_overdue(self):
        if self.status == RentalStatus.ACTIVE and self.is_overdue:
            self._transition(RentalStatus.OVERDUE)
    
    def to_dict(self) -> dict:
        return {
            "rental_id": self.rental_id,
            "vehicle_id": self.vehicle_id,
            "customer_id": self.customer_id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "rental_days": self.rental_days,
            "status": self.status.value,
            "total_price": str(self.total_price),
            "deposit_amount": str(self.deposit_amount),
            "created_at": self.created_at.isoformat(),
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "approved_by": self.approved_by,
            "rejection_reason": self.rejection_reason
        }
