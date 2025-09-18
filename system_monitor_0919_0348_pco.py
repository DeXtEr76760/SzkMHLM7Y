# 代码生成时间: 2025-09-19 03:48:31
import psutil
from quart import Quart, jsonify

# 创建 Quart 应用
app = Quart(__name__)

# 系统性能监控工具 API 路由
@app.route("/monitor", methods=["GET"])
def monitor_system():
    """
    监控系统性能并返回 CPU 和内存使用率。
    """
    try:
        # 获取 CPU 使用率
        cpu_usage = psutil.cpu_percent(interval=1)
        # 获取内存使用率
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        # 返回 JSON 数据
        return jsonify(
            {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage
            }
        )
    except Exception as e:
        # 错误处理
        return jsonify(
            {
                "error": str(e)
            },
            status=500
        )

# 运行 Quart 应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
