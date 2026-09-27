import importlib
import sys
from pathlib import Path
import pytest

# 1. 动态获取根目录并强制注入 sys.path（解决 pytest 执行时的导包问题）
BASE_DIR = Path(__file__).resolve()
while BASE_DIR.name and not (BASE_DIR / "pytest.ini").exists():
    BASE_DIR = BASE_DIR.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# 2. 动态导入带数字前缀的模块
client_module = importlib.import_module("02_common.client")
HTTPClient = client_module.HTTPClient


@pytest.fixture(scope="session")
def api_client():
    """提供给所有测试用例使用的 HTTPClient 实例"""
    client = HTTPClient()
    yield client