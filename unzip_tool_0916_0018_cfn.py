# 代码生成时间: 2025-09-16 00:18:20
import os
import zipfile
from quart import Quart

# 创建 Quart 应用
app = Quart(__name__)

# 解压文件的工具函数
def unzip_file(zip_path, extract_to):
    """
    解压 zip 文件到指定目录。
    :param zip_path: ZIP 文件的路径。
    :param extract_to: 解压到的目录路径。
    :return: None
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"文件 {zip_path} 解压成功，存放在 {extract_to}。")
    except zipfile.BadZipFile:
        print(f"错误：文件 {zip_path} 不是有效的 ZIP 文件。")
    except FileNotFoundError:
        print(f"错误：文件 {zip_path} 不存在。")
    except Exception as e:
        print(f"错误：解压过程中发生未知错误。{e}")

# Quart 路由处理压缩文件上传和解压
@app.route('/unzip', methods=['POST'])
async def unzip():
    """
    处理上传的压缩文件并解压。
    :return: JSON 响应
    """
    # 获取上传的文件
    file = await request.files.get('file')
    if not file:
        return jsonify({'error': '没有文件上传'})

    # 保存上传的文件
    save_path = os.path.join('uploads', file.filename)
    await file.save(save_path)

    # 解压文件
    extract_path = os.path.join('uploads', 'extracted')
    os.makedirs(extract_path, exist_ok=True)
    unzip_file(save_path, extract_path)

    # 返回成功响应
    return jsonify({'message': '文件解压成功'})

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)