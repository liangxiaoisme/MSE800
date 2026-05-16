"""
仓储模式（Repository Pattern）— 数据访问抽象层
解耦领域层与数据持久化实现，便于切换数据库技术
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session

T = TypeVar('T')
ID = TypeVar('ID')


class Repository(ABC, Generic[T, ID]):
    """
    泛型仓储接口
    所有具体仓储类必须实现此接口
    """
    
    @abstractmethod
    def get_by_id(self, id: ID) -> Optional[T]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def delete(self, id: ID) -> bool:
        pass
    
    @abstractmethod
    def exists(self, id: ID) -> bool:
        pass


class SQLAlchemyRepository(Repository[T, ID]):
    """
    SQLAlchemy 通用仓储基类
    提供基于 SQLAlchemy 的标准 CRUD 实现
    """
    
    def __init__(self, session: Session, model_class: type):
        self._session = session
        self._model_class = model_class
    
    def get_by_id(self, id: ID) -> Optional[T]:
        return self._session.query(self._model_class).filter_by(id=id).first()
    
    def get_all(self) -> List[T]:
        return self._session.query(self._model_class).all()
    
    def add(self, entity: T) -> T:
        self._session.add(entity)
        self._session.commit()
        return entity
    
    def update(self, entity: T) -> T:
        self._session.merge(entity)
        self._session.commit()
        return entity
    
    def delete(self, id: ID) -> bool:
        entity = self.get_by_id(id)
        if entity:
            self._session.delete(entity)
            self._session.commit()
            return True
        return False
    
    def exists(self, id: ID) -> bool:
        return self._session.query(self._model_class).filter_by(id=id).first() is not None
