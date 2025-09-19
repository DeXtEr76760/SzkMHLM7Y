# 代码生成时间: 2025-09-19 20:19:14
import quart
from zipfile import ZipFile
from quart import request, jsonify
import os
import shutil

# 定义压缩文件解压工具
class UnzipTool:
    def __init__(self, output_dir):
        """
        初始化解压工具
        :param output_dir: 解压后的文件存放目录
        """
        self.output_dir = output_dir

    def unzip_file(self, file_path):
        """
        解压文件
        :param file_path: 压缩文件路径
        :return: 解压结果
        """
        try:
            with ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(self.output_dir)
                return True, "文件解压成功"
        except Exception as e:
            return False, str(e)

# 创建Quart应用
app = quart.Quart(__name__)

@app.route('/unzip', methods=['POST'])
async def unzip():
    "