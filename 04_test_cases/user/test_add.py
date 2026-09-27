import importlib
import sys
from pathlib import Path
import pytest

# 同样加上这段根目录注入
BASE_DIR = Path(__file__).resolve()
while BASE_DIR.name and not (BASE_DIR / "pytest.ini").exists():
    BASE_DIR = BASE_DIR.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# 导入 YAML 解析与配置
yaml_handler = importlib.import_module("02_common.yaml_handler")
setting = importlib.import_module("01_config.setting")
logger_module = importlib.import_module("02_common.logger")

load_yaml = yaml_handler.load_yaml
logger = logger_module.logger

# 读取测试数据
test_data_path = BASE_DIR / "03_test_data" / "user" /"test_add.yaml"
cases = load_yaml(test_data_path)


class TestAddUser:
    """用户模块add接口测试集"""

    @pytest.mark.parametrize("case", cases)
    def test_add_user(self, api_client, case):
        """测试新增用户接口 (POST)"""
        logger.info(f"===== 开始执行用例: {case['title']} =====")

        # 发送 POST 请求，传入 json 参数
        response = api_client.request("POST", "/users", json=case["payload"])

        # 1. 校验状态码 (201 Created)
        assert response.status_code == case["expected_status"]

        # 2. 校验响应 Body
        res_json = response.json()
        assert "id" in res_json  # 断言返回体中包含自动生成的 id 字段
        if case["expected_status"] == 201 and "expected_name" in case:
            assert res_json["name"] == case["expected_name"]

        logger.info(f"===== 用例通过: {case['title']} =====\n")