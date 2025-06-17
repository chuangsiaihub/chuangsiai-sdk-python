# 开发环境搭建指南

本文档介绍如何使用 Python 自带的 `venv` 模块创建虚拟环境，并安装项目依赖，确保开发环境与生产环境隔离，方便统一管理依赖。

---

## 1. 创建虚拟环境

在项目根目录下执行以下命令，创建名为 `myenv` 的虚拟环境：

```bash
python3 -m venv myenv
```

## 2. 激活虚拟环境

根据操作系统不同，激活虚拟环境的命令略有区别：

- **Windows**：

```bash
myenv\Scripts\activate
```

- **macOS / Linux**：

```bash
source myenv/bin/activate
```

激活后，终端命令行提示符通常会显示虚拟环境名称，表示进入了隔离的 Python 环境。

## 3. 安装依赖包

虚拟环境激活后，安装项目依赖：

```bash
pip3 install -r requirements.txt
```

该命令会根据 `requirements.txt` 文件安装所有依赖库。

## 4. 打包项目

### 1. 准备

确保你的项目结构完整，有 pyproject.toml 或 setup.py。

```bash
pip3 install --upgrade build twine
```

### 2. 打包

在项目根目录运行：

```bash
python3 -m build
```

会生成 dist/ 目录，里面有 .tar.gz 和 .whl 文件。

### 3. 上传

TestPyPI 是 PyPI 的测试环境，避免误上传正式仓库。(文档)[https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives]

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

- 配置了`$HOME/.pypirc`可使用下面命令(文档)[https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#create-an-account]

```bash
twine upload --repository chuangsiai-sdk  dist/*
```

这时会提示你输入 TestPyPI 的用户名和密码。

- 正式版

```bash
 twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

### 4. 安装

```bash
pip3 install -i https://test.pypi.org/simple/ chuangsiai-sdk
```

pip3 install -e .

## 4. 项目目录结构

项目目录结构如下：

```
chuangsiai-sdk-python/
├── chuangsiai/
│   ├── __init__.py
│   ├── client.py          # 主客户端
│   ├── auth.py            # 认证模块
│   ├── exceptions.py      # 自定义异常
│   ├── models.py          # 数据模型
│   └── utils.py           # 工具函数
├── tests/                 # 单元测试
├── examples/              # 使用示例
├── setup.py
├── pyproject.toml
├── README.md
└── requirements.txt
```
