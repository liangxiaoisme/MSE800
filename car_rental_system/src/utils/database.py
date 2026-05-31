"""
单例模式 — 数据库连接管理器
确保全局只有一个数据库连接池实例，避免资源泄漏
"""

import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from contextlib import contextmanager


Base = declarative_base()


class DatabaseManager:
    """
    线程安全的单例数据库管理器
    使用双重检查锁定（Double-Checked Locking）确保并发安全
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, connection_string: str = "sqlite:///car_rental.db"):
        if cls._instance is None:
            with cls._lock:
                # 双重检查
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
                    cls._instance._connection_string = connection_string
        return cls._instance
    
    def _init_engine(self):
        if not self._initialized:
            self.engine = create_engine(
                self._connection_string,
                echo=False,           # 生产环境关闭SQL日志
                pool_pre_ping=True,   # 连接前ping检测，防止失效连接
                pool_recycle=3600     # 1小时回收连接
            )
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            self._initialized = True
    
    def get_engine(self):
        self._init_engine()
        return self.engine
    
    def get_session(self) -> Session:
        self._init_engine()
        return self.SessionLocal()
    
    @contextmanager
    def session_scope(self):
        """
        提供事务上下文管理器，自动处理提交和回滚
        使用示例:
            with db_manager.session_scope() as session:
                session.add(new_car)
                # 自动提交或回滚
        """
        self._init_engine()
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def create_tables(self):
        """根据模型定义创建所有数据表"""
        self._init_engine()
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """删除所有数据表（仅用于测试）"""
        self._init_engine()
        Base.metadata.drop_all(bind=self.engine)
    
    @classmethod
    def reset_instance(cls):
        """重置单例（仅用于单元测试）"""
        cls._instance = None


# 全局访问点
db_manager = DatabaseManager()
