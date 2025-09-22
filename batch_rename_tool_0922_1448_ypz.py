# 代码生成时间: 2025-09-22 14:48:24
import os
import re
from quart import Quart, request, jsonify

# 创建一个Quart应用
app = Quart(__name__)

# 定义一个正则表达式来匹配文件名
file_pattern = re.compile(r'^(\d+)_(.+)$')

# 定义一个函数用于重命名文件
def rename_files(directory, prefix):
    try:
        # 列出目录下的所有文件
        files = os.listdir(directory)
        renamed_files = []
        for file in files:
            # 使用正则表达式匹配文件名
            match = file_pattern.match(file)
            if match:
                new_filename = f"{prefix}_{match.group(1)}_{match.group(2)}"
                # 重命名文件
                os.rename(os.path.join(directory, file), os.path.join(directory, new_filename))
                renamed_files.append(new_filename)
        return renamed_files
    except Exception as e:
        return str(e)

# 定义一个路由用于处理POST请求
@app.route('/rename', methods=['POST'])
async def rename():
    try:
        # 获取POST请求的JSON数据
        data = await request.get_json()
        directory = data.get('directory')
        prefix = data.get('prefix')
        if not directory or not prefix:
            return jsonify({'error': 'Missing directory or prefix'}), 400
        # 调用重命名函数
        result = rename_files(directory, prefix)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 定义一个路由用于列出目录下的所有文件
@app.route('/files', methods=['GET'])
async def list_files():
    try:
        directory = request.args.get('directory')
        if not directory:
            return jsonify({'error': 'Missing directory'}), 400
        # 列出目录下的所有文件
        files = os.listdir(directory)
        return jsonify({'files': files}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 运行Quart应用
    app.run(debug=True)