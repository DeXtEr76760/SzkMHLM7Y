# 代码生成时间: 2025-09-21 11:26:01
from quart import Quart, jsonify, request

# 创建一个Quart应用实例
app = Quart(__name__)

# 模拟一个数据库，存储库存信息
inventory_db = {
    "items": [
        {
            "item_id": 1,
            "name": "Apple",
            "quantity": 100
        },
        {
            "item_id": 2,
            "name": "Banana",
            "quantity": 150
        }
    ]
}


# 获取所有库存项的路由
@app.route('/inventory', methods=['GET'])
async def get_inventory():
    # 返回所有库存项的JSON
    return jsonify(inventory_db)


# 获取单个库存项的路由
@app.route('/inventory/<int:item_id>', methods=['GET'])
async def get_item(item_id):
    # 查找指定ID的库存项
    for item in inventory_db['items']:
        if item['item_id'] == item_id:
            return jsonify(item)
    # 如果没有找到，返回404错误
    return jsonify({'error': 'Item not found'}), 404


# 添加库存项的路由
@app.route('/inventory', methods=['POST'])
async def add_item():
    # 解析请求体中的JSON数据
    data = await request.get_json()
    # 添加新的库存项
    inventory_db['items'].append(data)
    return jsonify(data), 201

# 更新库存项的路由
@app.route('/inventory/<int:item_id>', methods=['PUT'])
async def update_item(item_id):
    # 解析请求体中的JSON数据
    data = await request.get_json()
    # 查找并更新指定ID的库存项
    for item in inventory_db['items']:
        if item['item_id'] == item_id:
            item.update(data)
            return jsonify(item)
    # 如果没有找到，返回404错误
    return jsonify({'error': 'Item not found'}), 404

# 删除库存项的路由
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
async def delete_item(item_id):
    # 查找并删除指定ID的库存项
    global inventory_db
    inventory_db['items'] = [item for item in inventory_db['items'] if item['item_id'] != item_id]
    return jsonify({'message': 'Item deleted'})


# 运行应用
if __name__ == '__main__':
    app.run(debug=True)