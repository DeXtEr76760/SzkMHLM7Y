# 代码生成时间: 2025-09-20 17:24:10
import os
import shutil
from quart import Quart, jsonify, request

# 创建一个Quart应用
app = Quart(__name__)

# 定义配置参数
CONFIG = {
    "source_folder": "path/to/source_folder",
    "destination_folder": "path/to/destination_folder",
    "extensions_whitelist": [".jpg", ".png", ".txt", ".pdf"]
}

# 主要功能：整理文件夹结构
def clean_folder_structure(source, destination, extensions_whitelist):
    # 检查源文件夹是否存在
    if not os.path.exists(source):
        raise FileNotFoundError(f"Source folder {source} does not exist.")
    
    # 检查目标文件夹是否存在，如果不存在则创建
    os.makedirs(destination, exist_ok=True)

    # 遍历源文件夹
    for item in os.scandir(source):
        if item.is_file():
            # 检查文件扩展名是否在白名单
            _, extension = os.path.splitext(item.name)
            if extension.lower() in extensions_whitelist:
                # 移动文件到目标文件夹
                shutil.move(item.path, os.path.join(destination, item.name))
                print(f'Moved {item.name} to {destination}')
        elif item.is_dir():
            # 递归整理子文件夹
            clean_folder_structure(item.path, os.path.join(destination, item.name), extensions_whitelist)

# API路由：启动文件夹整理
@app.route('/clean', methods=['POST'])
async def clean():
    try:
        # 获取请求数据
        data = await request.get_json()
        source = data.get('source_folder')
        destination = data.get('destination_folder')
        extensions_whitelist = data.get('extensions_whitelist')
        
        # 调用整理函数
        clean_folder_structure(source, destination, extensions_whitelist)
        
        # 返回成功响应
        return jsonify({"message": "Folder structure cleaned successfully."}), 200
    except Exception as e:
        # 返回错误处理响应
        return jsonify({"error": str(e)}), 500

# 主函数，启动服务器
if __name__ == '__main__':
    app.run()
