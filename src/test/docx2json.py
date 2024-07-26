from docx import Document
import json  # 导入json模块
from JSONify_docx import doc_JSONify

doc = Document('./demobook2.docx')
json1 =  doc_JSONify(doc)

# 指定保存文件的路径
file_path = 'output.json'

# 将 JSON 字典保存到文件，以好看的格式
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(json1, f, indent=4, ensure_ascii=False)

print()