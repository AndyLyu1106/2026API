import importlib
import sys
from pathlib import Path
import pytest

# 1. 动态查找根目录
BASE_DIR = Path(__file__).resolve()
while BASE_DIR.name and not (BASE_DIR / "pytest.ini").exists():
    BASE_DIR = BASE_DIR.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# 2. 导入工具与配置
yaml_handler = importlib.import_module("02_common.yaml_handler")
setting = importlib.import_module("01_config.setting")
logger_module = importlib.import_module("02_common.logger")

load_yaml = yaml_handler.load_yaml
logger = logger_module.logger

# 3. 加载测试数据
test_data_path = BASE_DIR / "03_test_data" / "user" / "test_update.yaml"
cases = load_yaml(test_data_path)


class TestUpdateUser:
    """用户模块update接口测试集"""

    @pytest.mark.parametrize("case", cases)
    def test_update_user(self, api_client, case):
        logger.info(f"===== 开始执行用例: {case['title']} =====")

        # 动态指定请求方法 (PUT 或 PATCH)
        response = api_client.request(
            method=case["method"],
            url=f"/users/{case['user_id']}",
            json=case["payload"]
        )

        # 1. 校验状态码 200
        assert response.status_code == case["expected_status"]

        # 2. 校验更新后的字段
        res_json = response.json()
        if "expected_name" in case:
            assert res_json["name"] == case["expected_name"]
        if "expected_email" in case:
            assert res_json["email"] == case["expected_email"]

        logger.info(f"===== 用例通过: {case['title']} =====\n")