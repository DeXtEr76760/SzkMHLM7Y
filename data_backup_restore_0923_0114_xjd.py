# 代码生成时间: 2025-09-23 01:14:52
import shutil
import os
from quart import Quart, request, jsonify

# 创建一个Quart应用
app = Quart(__name__)

# 定义备份和恢复的文件路径
BACKUP_DIR = "./backups/"

# 确保备份目录存在
os.makedirs(BACKUP_DIR, exist_ok=True)

# 备份文件
@app.route("/backup", methods=["POST"])
async def backup():
    # 获取要备份的文件路径
    file_path = request.form.get("file_path")
    if not file_path:
        return jsonify(error="No file path provided"), 400
    
    # 验证文件存在
    if not os.path.exists(file_path):
        return jsonify(error="File not found"), 404
    
    try:
        # 创建备份文件名
        backup_file_name = f"{os.path.basename(file_path)}_backup_{datetime.now().isoformat()}"
        backup_file_path = os.path.join(BACKUP_DIR, backup_file_name)
        
        # 复制文件到备份目录
        shutil.copy2(file_path, backup_file_path)
        return jsonify(message=f"Backup created successfully: {backup_file_path}"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

# 恢复文件
@app.route("/restore", methods=["POST"])
async def restore():
    # 获取要恢复的备份文件路径
    backup_file_path = request.form.get("backup_file_path")
    if not backup_file_path:
        return jsonify(error="No backup file path provided"), 400
    
    # 验证备份文件存在
    if not os.path.exists(backup_file_path):
        return jsonify(error="Backup file not found"), 404
    
    try:
        # 获取备份文件的原始路径
        original_file_path = os.path.join(os.path.dirname(backup_file_path), os.path.basename(backup_file_path).split("_backup_")[0])
        
        # 恢复文件
        shutil.copy2(backup_file_path, original_file_path)
        return jsonify(message=f"File restored successfully: {original_file_path}"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

# 启动应用
if __name__ == '__main__':
    app.run()