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
test_data_path = BASE_DIR / "03_test_data" / "posts" / "test_delete.yaml"
cases = load_yaml(test_data_path)


class TestDeletePosts:
    """posts模块delete接口测试集"""

    @pytest.mark.parametrize("case", cases)
    def test_delete_posts(self, api_client, case):
        logger.info(f"===== 开始执行用例: {case['title']} =====")

        # 发送 DELETE 请求
        response = api_client.request("DELETE", f"/posts/{case['post_id']}")

        # 1. 校验状态码 200
        assert response.status_code == case["expected_status"]

        # 2. 断言返回体是否为空字典或符合 Mock 规范
        res_json = response.json()
        assert res_json == {}  # DELETE 操作通常返回空对象 {}

        logger.info(f"===== 用例通过: {case['title']} =====\n")