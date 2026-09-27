from pathlib import Path
import yaml


def load_yaml(file_path: str | Path) -> dict | list:
    """读取 YAML 文件并返回 Python 数据结构（字典或列表）

    :param file_path: 文件绝对路径或 Path 对象
    :return: 解析后的数据
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"YAML 配置文件未找到: {path.resolve()}")

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
            return data if data is not None else {}
        except yaml.YAMLError as e:
            raise ValueError(f"YAML 文件解析失败: {path.name}, 错误信息: {e}")