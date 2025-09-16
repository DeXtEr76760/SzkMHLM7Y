# 代码生成时间: 2025-09-16 12:07:48
import quart
from quart import jsonify
import psutil
import os

# 进程管理器
class ProcessManager:
    def __init__(self):
        pass

    # 获取所有进程
    def get_all_processes(self):
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                processes.append({'pid': proc.info['pid'], 'name': proc.info['name']})
            return processes
        except Exception as e:
            return {'error': str(e)}

    # 启动一个新进程
    def start_process(self, command):
        try:
            os.system(command)
            return {'message': 'Process started successfully'}
        except Exception as e:
            return {'error': str(e)}

    # 终止一个进程
    def terminate_process(self, pid):
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait()
            return {'message': 'Process terminated successfully'}
        except Exception as e:
            return {'error': str(e)}

# 创建Quart应用
app = quart.Quart(__name__)

# 定义路由和视图函数
@app.route('/processes', methods=['GET'])
async def get_processes():
    manager = ProcessManager()
    processes = manager.get_all_processes()
    if 'error' in processes:
        return jsonify(processes), 500
    return jsonify(processes)

@app.route('/start', methods=['POST'])
async def start_process():
    manager = ProcessManager()
    data = await quart.request.get_json()
    if 'command' not in data:
        return jsonify({'error': 'Missing command parameter'}), 400
    result = manager.start_process(data['command'])
    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result)

@app.route('/terminate/<int:pid>', methods=['POST'])
async def terminate_process(pid):
    manager = ProcessManager()
    result = manager.terminate_process(pid)
    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)