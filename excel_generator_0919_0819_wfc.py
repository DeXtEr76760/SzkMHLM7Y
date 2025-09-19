# 代码生成时间: 2025-09-19 08:19:57
import quart
from quart import jsonify
import pandas as pd
from io import StringIO
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

# 定义Excel生成器类
class ExcelGenerator:
# 改进用户体验
    def __init__(self):
        self.data = []

    def add_data(self, data):
        """
        添加数据到列表中
        :param data: 要添加的数据列表，格式为[{'column1': 'value1', 'column2': 'value2'}, ...]
        """
        if not isinstance(data, list):
            raise ValueError("数据必须是列表类型")
        self.data.extend(data)

    def generate_excel(self):
        """
        生成Excel文件
        :return: 生成的Excel文件内容
        """
        try:
# 增强安全性
            # 使用pandas创建DataFrame
            df = pd.DataFrame(self.data)

            # 将DataFrame转换为Excel文件
            excel_buffer = StringIO()
            df.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)

            # 将Excel文件内容保存到Workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "Sheet1"

            # 读取Excel文件内容并写入Workbook
            reader = pd.read_excel(excel_buffer)
            for r, row in reader.iterrows():
# TODO: 优化性能
                for c, value in enumerate(row):
                    ws.cell(row=r+1, column=c+1, value=value)

            # 将Workbook保存为虚拟文件
            return save_virtual_workbook(wb)
        except Exception as e:
            raise Exception("生成Excel文件失败: " + str(e))

# 定义Quart应用
app = quart.Quart(__name__)

# 定义路由，生成并返回Excel文件
@app.route("/generate_excel", methods=["POST"])
async def generate_excel_api():
    data = quart.request.json
    try:
        generator = ExcelGenerator()
        generator.add_data(data)
        excel_content = generator.generate_excel()
        return quart.Response(excel_content, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 启动Quart应用
if __name__ == '__main__':
    app.run()
