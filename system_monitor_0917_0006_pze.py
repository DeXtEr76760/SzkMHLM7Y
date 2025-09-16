# 代码生成时间: 2025-09-17 00:06:32
import psutil
from quart import Quart, jsonify

# 创建Quart应用
app = Quart(__name__)

# 系统性能监控工具
class SystemMonitor:
    def get_system_info(self):
        '''
        获取系统信息
        '''
        info = {
            "cpu_percentage": psutil.cpu_percent(),
            "memory_percentage": psutil.virtual_memory().percent,
            "disk_percentage": psutil.disk_usage('/').percent,
            "network_in": psutil.net_io_counters().bytes_recv,
            "network_out": psutil.net_io_counters().bytes_sent,
        }
        return info

    def get_process_info(self, process_name):
        '''
        获取指定进程信息
        '''
        try:
            process = psutil.Process(process_name)
            info = {
                "pid": process.pid,
                "cpu_percentage": process.cpu_percent(),
                "memory_percentage": process.memory_percent(),
            }
            return info
        except psutil.NoSuchProcess:
            return {"error": "Process not found"}

# 路由和视图函数
@app.route("/system-info")
async def get_system_info():
    '''
    获取系统信息
    '''
    monitor = SystemMonitor()
    info = monitor.get_system_info()
    return jsonify(info)

@app.route("/process-info/<process_name>")
async def get_process_info(process_name):
    '''
    获取指定进程信息
    '''
    monitor = SystemMonitor()
    info = monitor.get_process_info(process_name)
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True)