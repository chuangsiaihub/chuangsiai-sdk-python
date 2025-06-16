from typing import Optional

class ChuangSiAiSafetyException(Exception):
    """SDK基础异常"""
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(message)
        self.cause = cause

class AuthenticationException(ChuangSiAiSafetyException):
    """认证异常"""
    pass

class APIException(ChuangSiAiSafetyException):
    """API请求异常"""
    def __init__(self, status_code: int, message: str):
        super().__init__(f"[{status_code}] {message}")
        self.status_code = status_code

class ValidationException(ChuangSiAiSafetyException):  # 新增验证异常
    """请求参数验证异常"""
    pass