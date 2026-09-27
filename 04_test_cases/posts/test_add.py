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
test_data_path = BASE_DIR / "03_test_data" / "posts" /"test_add.yaml"
cases = load_yaml(test_data_path)

class TestAddPosts:
    """Posts模块add接口测试集"""

    @pytest.mark.parametrize("case", cases)
    def test_add_posts(self, api_client, case):
        """测试新增Posts信息"""
        logger.info(f"===== 开始执行用例: {case['title']} =====")
        response = api_client.request("POST", f"/posts", json=case["payload"])

        # 断言响应状态码
        assert response.status_code == case["expected_status"]

        # 若正常返回，继续校验 Body 字段
        res_json = response.json()
        assert "id" in res_json  # 断言返回体中包含自动生成的 id 字段
        if case["expected_status"] == 201 and "expected_title" in case:
            assert res_json["title"] == case["expected_title"]
            assert res_json["body"] == case["expected_body"]

        logger.info(f"===== 用例通过: {case['title']} =====\n")