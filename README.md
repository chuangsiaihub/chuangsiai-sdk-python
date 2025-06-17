# 创思大模型安全工具 SDK 使用说明

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/chuangsiai-sdk.svg)](https://pypi.org/project/chuangsiai-sdk/)

> 创思大模型安全工具是一款面向大语言模型的内容安全防护 SDK，致力于识别和拦截潜在的输入输出风险，确保大模型的使用安全、合规、可信。

---

## ✨ 功能概述

- ✅ 输入内容安全检测（Input Safety Guardrail）
- ✅ 输出内容安全检测（Output Safety Guardrail）
- ✅ 支持高性能异步请求
- ✅ 易于集成到各类 Python 应用中

---

## 📦 安装

### 使用 pip 安装：

```bash
pip3 install requests pydantic chuangsiai-sdk
```

### 源码安装：

```bash
git clone https://github.com/chuangsiaihub/chuangsiai-sdk.git
cd chuangsiai-sdk
pip3 install -e .

```

## 🚀 快速上手

```python
from chuangsiai_sdk import ChuangsiaiClient

def main():
    client = ChuangsiaiClient(access_key="< 控制台申请的 AccessKey >",secret_key="< 控制台申请的 SecretKey >")

    resp =  client.input_guardrail(strategy_key="< 策略标识，在控制台中创建 >", content="检测文本")

    print(resp)

if __name__ == "__main__":
    main()

```

## 📚 文档说明

- [使用示例 1](https://github.com/chuangsiaihub/chuangsiai-sdk-python/blob/master/examples/accesskey_simple_usage.py)、[使用示例 2](https://github.com/chuangsiaihub/chuangsiai-sdk-python/blob/master/examples/apikey_simple_usage.py)

- [开发指南](https://github.com/chuangsiaihub/chuangsiai-sdk-python/blob/master/DEVELOPMENT.md)

## 🛠️ 开发环境搭建

```bash
# 创建并激活虚拟环境
python3 -m venv myenv
source myenv/bin/activate

# 安装开发依赖
pip3 install -r requirements.txt

# 安装本地包（可编辑模式）
pip3 install -e .

```

更多开发细节请参考 [DEVELOPMENT.md](https://github.com/chuangsiaihub/chuangsiai-sdk-python/blob/master/DEVELOPMENT.md)。

## 🔐 安全策略

创思安全 SDK 依赖 HMAC-SHA256 签名机制对所有请求进行身份验证和防篡改处理。详见 [auth.py](https://github.com/chuangsiaihub/chuangsiai-sdk-python/blob/master/chuangsiai_sdk/auth.py)。

## 📦 依赖列表

- requests >= 2.25.0
- pydantic >= 2.0.0

## 📄 许可证

本项目基于 MIT 协议开源。

## 📬 联系我们

如需技术支持、企业合作或 API 接入，请联系：

- 邮箱: service@chuangsiai.com
- 官网: https://chuangsiai.com
- 控制台: https://console.chuangsiai.com

---

**让大模型更安全、更可信 —— 创思大模型安全。**
