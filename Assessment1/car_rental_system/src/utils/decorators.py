"""
装饰器模式 — 基于角色的访问控制（RBAC）
采用 Python 函数装饰器实现横切关注点（Cross-cutting Concerns）
"""

from functools import wraps
from typing import List, Callable
from flask import session, redirect, url_for, jsonify


class AuthorizationError(Exception):
    """权限不足异常"""
    pass


def require_role(allowed_roles: List[str]):
    """
    角色验证装饰器
    
    使用示例:
        @app.route('/admin/cars')
        @require_role(['admin', 'fleet_manager'])
        def manage_cars():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 检查登录状态
            if 'user_id' not in session:
                if request.is_json:
                    return jsonify({"error": "Unauthorized", "code": 401}), 401
                return redirect(url_for('login'))
            
            # 检查角色权限
            user_role = session.get('role')
            if user_role not in allowed_roles:
                if request.is_json:
                    return jsonify({
                        "error": "Forbidden",
                        "message": f"Required roles: {allowed_roles}",
                        "your_role": user_role,
                        "code": 403
                    }), 403
                return redirect(url_for('unauthorized'))
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_permission(required_permission: str):
    """
    细粒度权限验证装饰器
    基于权限字符串而非角色，更灵活
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({"error": "Unauthorized", "code": 401}), 401
            
            user_permissions = session.get('permissions', [])
            if required_permission not in user_permissions:
                return jsonify({
                    "error": "Permission Denied",
                    "required": required_permission,
                    "code": 403
                }), 403
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def login_required(func: Callable) -> Callable:
    """登录状态验证装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


def audit_log(action: str):
    """
    审计日志装饰器 — 自动记录敏感操作
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = session.get('user_id', 'anonymous')
            result = func(*args, **kwargs)
            print(f"[AUDIT] User={user_id} Action={action} Args={kwargs}")
            return result
        return wrapper
    return decorator


def rate_limit(max_requests: int = 100, window_seconds: int = 60):
    """
    速率限制装饰器 — 防止API滥用
    （简化实现，生产环境应使用 Redis）
    """
    from time import time
    requests = {}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = session.get('user_id', request.remote_addr)
            now = time()
            
            # 清理过期记录
            if user_id in requests:
                requests[user_id] = [t for t in requests[user_id] if now - t < window_seconds]
            else:
                requests[user_id] = []
            
            if len(requests[user_id]) >= max_requests:
                return jsonify({"error": "Rate limit exceeded", "code": 429}), 429
            
            requests[user_id].append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
