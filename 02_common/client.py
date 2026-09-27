import requests
import importlib

setting = importlib.import_module("01_config.setting")
logger_module = importlib.import_module("02_common.logger")
BASE_URL = setting.BASE_URL
TIMEOUT = setting.TIMEOUT
logger = logger_module.logger


class HTTPClient:
    """HTTP 请求客户端二次封装类"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        # 设置默认请求头
        self.session.headers.update({
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "APITest-Automation-Framework"
        })

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """统一发送请求的方法

        :param method: 请求方式 (GET, POST, PUT, DELETE)
        :param url: 接口相对路径 (例如 "/users/1")
        :param kwargs: requests 接受的其他参数 (headers, params, json, data 等)
        :return: requests.Response 对象
        """
        # 补全相对路径
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"

        # 确保包含超时设置
        kwargs.setdefault("timeout", TIMEOUT)

        logger.info(f"\n[Request] ---> {method.upper()} {full_url}")
        if "json" in kwargs:
            logger.info(f"[Request Body] : {kwargs['json']}")

        try:
            response = self.session.request(method, full_url, **kwargs)
            logger.info(f"[Response] <--- Status: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"[Request Error] : {e}")
            raise

# if __name__ == "__main__":
#     client = HTTPClient()
#     res = client.request("GET", "/users/1")
#     print("返回内容:", res.json()["name"])
