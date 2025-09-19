# 代码生成时间: 2025-09-20 00:28:13
import quart as q
from quart import request, jsonify
from marshmallow import Schema, fields, ValidationError, validates_schema
from marshmallow.validate import Email


# 表单数据验证器
class UserRegistrationSchema(Schema):
    """用户注册表单验证器"""
    name = fields.Str(required=True, validate=lambda x: x.isalpha(), error_messages={
        'required': 'Please provide your name.',
        'validate': 'Name must contain only letters.'
    })
    email = fields.Email(required=True, validate=Email(), error_messages={'required': 'Please provide your email.'})
    password = fields.Str(required=True, error_messages={'required': 'Please provide your password.'})
    confirm_password = fields.Str(required=True, validate=lambda x, y: x == y, error_messages={'required': 'Please confirm your password.'})
    password.register_attribute('confirm_password')

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError('Passwords do not match.')


# 创建Quart应用
app = q.Quart(__name__)

# 用户注册路由
@app.route('/register', methods=['POST'])
async def register():
    try:
        # 获取表单数据
        data = await request.get_json()
        # 创建验证器实例并验证数据
        validator = UserRegistrationSchema()
        result = validator.load(data)
        return jsonify({'message': 'Registration successful!'}), 200
    except ValidationError as err:
        # 返回验证错误信息
        return jsonify({'errors': err.messages}), 400
    except Exception as e:
        # 返回通用错误信息
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
