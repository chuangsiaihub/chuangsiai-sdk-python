# examples/accesskey_simple_usage.py
from chuangsiai_sdk import ChuangsiaiClient

def main():
    # 初始化客户端
    client = ChuangsiaiClient(access_key="< 控制台申请的 AccessKey >",secret_key="< 控制台申请的 SecretKey >")
    
    # 调用接口
    resp =  client.input_guardrail(strategy_id="< 策略标识，在控制台中创建 >", content="检测文本")
    
    # 处理返回结果。这里简单打印
    print("接口返回:", resp)

if __name__ == "__main__":
    main()
