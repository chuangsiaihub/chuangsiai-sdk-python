import hmac
import hashlib
import json
import time
import uuid
from urllib.parse import quote
from typing import Optional, Dict, Any
from .exceptions import AuthenticationException  

class AuthGenerator:
    def __init__(
        self, 
        api_key: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None
    ):
        """
        初始化认证生成器，根据参数自动选择认证方式
        
        认证方式选择规则:
        1. 如果提供了 api_key，则使用 API_KEY 认证
        2. 如果提供了 access_key 和 secret_key，则使用 ACCESS_KEY 签名认证
        3. 如果未提供任何有效凭证，抛出异常
        
        :param api_key: API_KEY认证所需的密钥
        :param access_key: ACCESS_KEY认证所需的访问密钥
        :param secret_key: ACCESS_KEY认证所需的秘密密钥
        """
        if api_key:
            self.auth_type = "API_KEY"
            self.api_key = api_key
        elif access_key and secret_key:
            self.auth_type = "ACCESS_KEY"
            self.access_key = access_key
            self.secret_key = secret_key
        else:
            # 使用自定义异常
            raise AuthenticationException(
                "必须提供有效的认证凭证：\n"
                "1. 仅提供 api_key 用于简单认证\n"
                "2. 同时提供 access_key 和 secret_key 用于签名认证"
            )

    def generate_headers(
        self,
        method: str,
        url: str,
        body: Optional[Dict[str, Any]] = None,
        timestamp: Optional[int] = None,
        nonce: Optional[str] = None
    ) -> Dict[str, str]:
        """
        生成请求头
        
        :param method: HTTP方法 (GET/POST等)
        :param url: 请求URL路径
        :param body: 请求体字典
        :param timestamp: 时间戳(毫秒)，可选
        :param nonce: 随机字符串，可选
        :return: 请求头字典
        """
        headers = {'Content-Type': 'application/json'}
        
        if self.auth_type == "ACCESS_KEY":
            return self._generate_signed_headers(method, url, body, timestamp, nonce, headers)
        else:
            return self._generate_api_key_headers(headers)

    def _generate_signed_headers(
        self,
        method: str,
        url: str,
        body: Optional[Dict[str, Any]],
        timestamp: Optional[int],
        nonce: Optional[str],
        base_headers: Dict[str, str]
    ) -> Dict[str, str]:
        """生成签名认证头"""
        # 生成时间戳和随机数
        ts = timestamp or int(time.time() * 1000)
        nc = nonce or uuid.uuid4().hex
        
        # 生成签名
        signature = self._generate_signature(
            method=method,
            url=url,
            body=body,
            timestamp=ts,
            nonce=nc
        )
        
        # 组装头信息
        base_headers.update({
            'X-Timestamp': str(ts),
            'X-Nonce': nc,
            'Authorization': f"{self.access_key}:{signature}",
            'X-Referer': 'python-sdk-accesskey',
        })
        return base_headers

    def _generate_api_key_headers(self, base_headers: Dict[str, str]) -> Dict[str, str]:
        """生成API Key认证头"""
        base_headers.update({
            'Authorization': f"Bearer {self.api_key}",
            'X-Referer': 'python-sdk-apikey',
        })
        return base_headers

    def _generate_signature(
        self,
        method: str,
        url: str,
        body: Optional[Dict[str, Any]],
        timestamp: int,
        nonce: str
    ) -> str:
        """
        生成HMAC-SHA256签名
        
        :param method: HTTP方法
        :param url: 请求URL路径
        :param body: 请求体字典
        :param timestamp: 时间戳(毫秒)
        :param nonce: 随机字符串
        :return: 签名字符串
        """
        # 添加空body处理
        if body is None:
            body_string = ""
        else:
            try:
                ## 确保JSON紧凑无空格，避免签名不一致，并URL编码
                body_string = quote(json.dumps(body, ensure_ascii=False, separators=(',', ':')))
            except (TypeError, ValueError) as e:
                 # 添加异常处理
                raise AuthenticationException(f"请求体序列化失败: {str(e)}")
        
        # 拼接待签名字符串（严格按顺序）
        string_to_sign = f"{method}\n{url}\n{body_string}\n{timestamp}\n{nonce}"
        
        try:
            # 添加编码异常处理
            hmac_obj = hmac.new(
                self.secret_key.encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha256
            )
            return hmac_obj.hexdigest()
        except Exception as e:
            raise AuthenticationException(f"签名生成失败: {str(e)}")