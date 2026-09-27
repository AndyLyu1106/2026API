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
test_data_path = BASE_DIR / "03_test_data" / "user" /"test_query.yaml"
cases = load_yaml(test_data_path)


class TestQueryUser:
    """用户模块query接口测试集"""

    @pytest.mark.parametrize("case", cases)
    def test_get_user_by_id(self, api_client, case):
        """测试根据 ID 获取用户信息"""
        logger.info(f"===== 开始执行用例: {case['title']} =====")
        response = api_client.request("GET", f"/users/{case['user_id']}")

        # 断言响应状态码
        assert response.status_code == case["expected_status"]

        # 若正常返回，继续校验 Body 字段
        if case["expected_status"] == 200:
            res_json = response.json()
            assert res_json["name"] == case["expected_name"]
        logger.info(f"===== 用例通过: {case['title']} =====\n")

    def test_get_all_users(self, api_client):
        logger.info(f"===== 开始执行用例: 获取全部用户列表 =====")
        """测试获取全部用户列表"""
        response = api_client.request("GET", "/users")
        assert response.status_code == 200
        res_json = response.json()
        assert isinstance(res_json, list)
        assert len(res_json) == 10
        logger.info(f"===== 用例通过: 获取全部用户列表 =====\n")