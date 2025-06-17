import unittest
from unittest.mock import patch, MagicMock
from chuangsiai_sdk.client import ChuangsiaiClient
from chuangsiai_sdk.exceptions import APIException, ChuangSiAiSafetyException

class TestChuangsiaiClient(unittest.TestCase):
    def setUp(self):
        self.client = ChuangsiaiClient(api_key="test_api_key")

    @patch('chuangsiai.client.requests.Session.request')
    def test_input_guardrail_success(self, mock_request):
        # 模拟返回正常JSON
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {"result": "safe"}
        mock_request.return_value = mock_response

        resp = self.client.input_guardrail(strategy_key="default_strategy", content="测试内容")
        self.assertEqual(resp, {"result": "safe"})
        mock_request.assert_called_once()

    @patch('chuangsiai.client.requests.Session.request')
    def test_api_error_raises_exception(self, mock_request):
        # 模拟API返回错误JSON
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "错误信息"}
        mock_request.return_value = mock_response

        with self.assertRaises(APIException) as cm:
            self.client.input_guardrail(strategy_key="default_strategy", content="测试内容")
        self.assertIn("API Error", str(cm.exception))

    # @patch('chuangsiai.client.requests.Session.request')
    # def test_api_error_raises_exception_non_json(self, mock_request):
    #     # 模拟API返回错误非JSON响应
    #     mock_response = MagicMock()
    #     mock_response.ok = False
    #     mock_response.status_code = 500
    #     mock_response.json.side_effect = Exception("解析错误")
    #     mock_response.text = "服务器内部错误"
    #     mock_request.return_value = mock_response

    #     with self.assertRaises(APIException) as cm:
    #         self.client.input_guardrail(strategy_key="default_strategy", content="测试内容")
    #     self.assertIn("API Error", str(cm.exception))

    # @patch('chuangsiai.client.requests.Session.request')
    # def test_network_error_raises_exception(self, mock_request):
    #     # 模拟请求抛出网络异常
    #     mock_request.side_effect = Exception("连接超时")

    #     with self.assertRaises(ChuangSiAiSafetyException) as cm:
    #         self.client.input_guardrail(strategy_key="default_strategy", content="测试内容")
    #     self.assertIn("网络请求失败", str(cm.exception))


if __name__ == '__main__':
    unittest.main()
