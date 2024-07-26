import base64
import logging
from typing import Dict, Any

from JSONify_docx.dwml import omml
from JSONify_docx.elements import el


class math(el):
    __type__ = "formulas"

    def __init__(self, x):
        self.latex = ''
        try:
            load = omml.load_math_element(x)
            for math in load:
                latex = math.latex
                self.latex = '$' + latex + '$'
        except Exception as e:  # 公式解析存在异常
            logging.error("An error occurred while processing the OMML data: %s", str(e))
            self.latex = '$\\text{公式解析错误,请手动录入}$'



    def to_json(self, doc) -> Dict[str, Any]:
        out = {"type": "text", "text": self.latex}
        return out


class mathParagraph(el):
    __type__ = "formulas"          #word中保留了这个标签，还没调研清楚如何使用

    def __init__(self, x):
        self.latex = ''

        try:
            load = omml.load_math_paragraph_element(x)
            for math in load:
                latex = math.latex
                self.latex = '$' + latex + '$'
        except Exception as e:  # 捕获所有Exception基类的异常
            logging.error("An error occurred while processing the OMML data: %s", str(e))


    def to_json(self, doc) -> Dict[str, Any]:
        out = {"type": "text", "text": self.latex}
        return out


class embObject(el):
    __type__ = "embObject"
    def __init__(self, x):
        imagedata_element = x.xpath('.//v:imagedata', namespaces=x.nsmap)
        imagedata_element = imagedata_element[0]
        rId = imagedata_element.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        self.rId = rId


    def to_json(self, doc) -> Dict[str, Any]:
        out =  super().to_json(doc)
        if self.rId:
            rel = doc.part.rels[self.rId]
            image_part = rel.target_part
            data = image_part.blob
            ext = rel.target_ref.split('.')[-1]  # 获取扩展名
            # 通过rId直接获取对应的图像数据
            # image_part = doc.part.rels.get(self.rId).target_part
            # image_data = image_part.blob


            base64_data = base64.b64encode(data).decode('utf-8')

            temp = {"blob": base64_data, "ext": ext}
            out.update(temp)
            return out
