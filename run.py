from datetime import datetime
import subprocess
import pytest

if __name__ == "__main__":
    # 1. 运行 pytest 测试用例
    pytest.main()

    # 2. 生成当前时间戳格式 (例如: 20260918_103000)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 3. 动态拼接本次运行的报告目录名称
    target_report_dir = f"./reports/allure-report_{timestamp}"

    # 4. 调用 allure 生成独立时间戳的 HTML 报告
    cmd = f"allure generate ./reports/allure-results -o {target_report_dir} --clean"

    print(f"\n[System] 正在生成本次测试报告至: {target_report_dir} ...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"[System] 报告生成成功！保存路径为: {target_report_dir}")
    else:
        print(f"[System] 报告生成失败，错误信息:\n{result.stderr}")