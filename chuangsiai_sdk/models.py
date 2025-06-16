from pydantic import BaseModel, Field, ValidationError, model_validator

class BaseRequestModel(BaseModel):
    """基础请求模型"""
    def to_dict(self):
        return self.model_dump(exclude_none=True)

class InputGuardrailRequest(BaseRequestModel):
    strategyKey: str = Field(..., description="策略标识符")
    content: str = Field(..., description="待检测内容")

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, data):
        if not isinstance(data, dict):
            raise TypeError("数据格式必须是 dict")
        
        expected_fields = {"strategyKey", "content"}
        missing = expected_fields - data.keys()
        extra = data.keys() - expected_fields
        if missing:
            raise ValueError(f"❌ 缺少字段：{missing}")
        if extra:
            raise ValueError(f"❌ 存在无效字段：{extra}")

        return data


    # 模型验证示例
    class Config:
        json_schema_extra = {
            "example": {
                "strategyKey": "default_strategy",
                "content": "用户输入内容"
            }
        }

class OutputGuardrailRequest(BaseRequestModel):
    """安全护栏输出请求模型"""
    strategyKey: str = Field(..., description="策略标识符")
    content: str = Field(..., description="待检测内容")

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, data):
        if not isinstance(data, dict):
            raise TypeError("数据格式必须是 dict")
        
        expected_fields = {"strategyKey", "content"}
        missing = expected_fields - data.keys()
        extra = data.keys() - expected_fields
        if missing:
            raise ValueError(f"❌ 缺少字段：{missing}")
        if extra:
            raise ValueError(f"❌ 存在无效字段：{extra}")

        return data

    # 模型验证示例
    class Config:
        json_schema_extra = {
            "example": {
                "strategyKey": "default_strategy",
                "content": "AI生成内容"
            }
        }