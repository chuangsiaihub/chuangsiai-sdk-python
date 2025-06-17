import json
import os
import requests
from configparser import ConfigParser
from typing import Optional
from .auth import AuthGenerator
from .models import InputGuardrailRequest, OutputGuardrailRequest
from .exceptions import ChuangSiAiSafetyException, APIException, AuthenticationException

# 初始化解析器
config_path = os.path.join(os.path.dirname(__file__), "config.ini")
config = ConfigParser()
config.read(config_path)
# 读取配置
default_url = config.get("default", "base_url")
inputGuardrailApi = config.get("default", "input_guardrail_api")
outputGuardrailApi = config.get("default", "output_guardrail_api")
default_timeout = config.getint("default", "default_timeout")


class ChuangsiaiClient:
    BASE_URL = default_url
    DEFAULT_TIMEOUT = default_timeout  # 默认超时时间    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        timeout: float = default_timeout , # 超时参数
        base_url: str = default_url # 基础URL
    ):
        """
        初始化安全客户端，根据参数自动选择认证方式
        
        认证方式选择规则:
        1. 如果提供了 api_key，则使用 API_KEY 认证
        2. 如果提供了 access_key 和 secret_key，则使用 ACCESS_KEY 签名认证
        
        :param api_key: API_KEY认证所需的密钥
        :param access_key: ACCESS_KEY认证所需的访问密钥
        :param secret_key: ACCESS_KEY认证所需的秘密密钥
        """
        self.auth = AuthGenerator(
            api_key=api_key,
            access_key=access_key,
            secret_key=secret_key
        )
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "chuangsiai-python-SDK/1.0"})
        self.timeout = timeout  # 存储超时时间
        self.base_url = base_url  # 存储基础URL
    
    def _make_request(self, method: str, endpoint: str, payload: dict = None):
        """执行签名请求"""
        url = f"{self.base_url}{endpoint}"
        
        # 生成认证头
        try:
            headers = self.auth.generate_headers(
                method=method,
                url=endpoint, # 仅使用路径部分
                body=payload
            )
        except AuthenticationException as e:
            # 捕获并重新抛出认证异常
            raise ChuangSiAiSafetyException(f"认证头生成失败: {str(e)}")
        
        
        try:
            # 添加超时参数
            response = self.session.request(
                method=method,
                url=url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            # 处理响应
            if not response.ok:
                # 尝试解析错误信息
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', response.text)
                except json.JSONDecodeError:
                    error_msg = response.text
                # 使用更具体的异常类型
                raise APIException(
                    status_code=response.status_code, 
                    message=f"Cuangsiai API Error: {error_msg}"
                )
                
            return response.json()
        except requests.exceptions.RequestException as e:
            # 捕获所有网络异常
            raise ChuangSiAiSafetyException(f"网络请求失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise ChuangSiAiSafetyException(f"响应解析失败: {str(e)}")
    
    
    def input_guardrail(self, strategy_key: str, content: str) -> dict:
        """
        输入安全护栏内容检测
        
        :param strategy_key: 策略标识
        :param content: 检测内容
        """
        request = InputGuardrailRequest(strategy_key=strategy_key, content=content)
        return self._make_request(
            method="POST",
            endpoint=inputGuardrailApi,
            payload=request.to_dict()
        )
    
    def output_guardrail(self, strategy_key: str, content: str) -> dict:
        """
        输出安全护栏内容检测
        
        :param strategy_key: 策略标识
        :param content: 检测内容
        """
        request = OutputGuardrailRequest(strategy_key=strategy_key, content=content)
        return self._make_request(
            method="POST",
            endpoint=outputGuardrailApi,
            payload=request.to_dict()
        )