import os
import sys
from pathlib import Path

# 1. 自动将项目根目录加入 Python 搜索路径（最先执行！）
BASE_DIR = Path(__file__).resolve()
while BASE_DIR.name and not (BASE_DIR / "pytest.ini").exists():
    BASE_DIR = BASE_DIR.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# 2. 导入自定义工具（放在 sys.path 调整之后）
import importlib
yaml_handler = importlib.import_module("02_common.yaml_handler")
load_yaml = yaml_handler.load_yaml

# 3. 读取 env.yaml 配置
ENV_FILE = BASE_DIR / "01_config" / "env.yaml"
_config_data = load_yaml(ENV_FILE)

# 4. 动态确定当前生效的环境
ACTIVE_ENV = os.environ.get("ENV", _config_data.get("default_env", "test"))

# 5. 获取当前环境参数并导出
_CURRENT_ENV_CONFIG = _config_data["environments"][ACTIVE_ENV]
BASE_URL = _CURRENT_ENV_CONFIG["base_url"]
TIMEOUT = _CURRENT_ENV_CONFIG.get("timeout", 10)

# print(f"当前生效环境: {ACTIVE_ENV}")
# print(f"全局 BASE_URL: {BASE_URL}")