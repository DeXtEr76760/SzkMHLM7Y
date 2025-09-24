# 代码生成时间: 2025-09-24 15:31:44
import quart as q
from quart import jsonify, request
from collections import defaultdict

# 模拟数据库存储用户权限信息
user_permissions = defaultdict(set)

# 权限管理 API 的基类
class PermissionAPI:
    def __init__(self):
        pass

    def add_permission(self, username, permission):
        """
        添加用户权限
        :param username: 用户名
        :param permission: 权限
        """
        if username not in user_permissions:
            user_permissions[username] = set()
        user_permissions[username].add(permission)
        return jsonify({'status': 'success', 'message': 'Permission added'}), 200

    def remove_permission(self, username, permission):
        """
        移除用户权限
        :param username: 用户名
        :param permission: 权限
        """
        if username in user_permissions and permission in user_permissions[username]:
            user_permissions[username].remove(permission)
            return jsonify({'status': 'success', 'message': 'Permission removed'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'User or permission not found'}), 404

    def get_permissions(self, username):
        """
        获取用户权限
        :param username: 用户名
        """
        permissions = user_permissions.get(username, set())
        return jsonify({'status': 'success', 'data': list(permissions)}), 200

# 创建 Quart 应用
app = q.Quart(__name__)

# 实例化权限 API 类
permission_api = PermissionAPI()

@app.route('/add_permission', methods=['POST'])
async def add_permission():
    """
    添加用户权限的接口
    """
    username = request.json.get('username')
    permission = request.json.get('permission')
    return permission_api.add_permission(username, permission)

@app.route('/remove_permission', methods=['POST'])
async def remove_permission():
    """
    移除用户权限的接口
    """
    username = request.json.get('username')
    permission = request.json.get('permission')
    return permission_api.remove_permission(username, permission)

@app.route('/get_permissions', methods=['GET'])
async def get_permissions():
    """
    获取用户权限的接口
    """
    username = request.args.get('username')
    return permission_api.get_permissions(username)

# 启动应用
if __name__ == '__main__':
    app.run(debug=True)