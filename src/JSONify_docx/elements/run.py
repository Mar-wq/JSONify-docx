import re
from typing import Dict, Any, Optional

import webcolors
from more_itertools import peekable
from . import el, container
class run(container):
    __type__ = "run"
    def __init__(self, x):
        super().__init__(x)
        self.out = {"type": None}

    def to_json(self, doc) -> Dict[str, Any]:

        iter_me = peekable(self)
        for elt in iter_me:
            JSON = elt.to_json(doc)
            if JSON:
                self.out.update(JSON)

        return self.out


class commentReference(el):
    __type__ = "commentReference"

    def __init__(self, x):
        self.props = {}
        namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        rId = x.xpath('@w:id', namespaces=namespaces)[0]
        self.props['rId'] = rId
        print()

class rPr(container):
    __type__ = "rPr"
    def to_json(self, doc) -> Dict[str, Any]:
        """Coerce a container object to JSON
        """
        marks = []
        for elt in self:
            JSON = elt.to_json(doc)

            if JSON:
                marks.append(JSON)

        # out: Dict[str, Any] = {"TYPE": self.__type__, "VALUE": contents}
        if marks:
            return {"marks": marks}
        return {}

class text(el):
    def to_json(self, doc) -> Dict[str, Any]:
        return {"type": "text", "text": self.fragment.text}



class underline(el):
    def to_json(self, doc) -> Dict[str, Any]:
        return {"type": "underline"}


class italic(el):
    def to_json(self, doc) -> Dict[str, Any]:
        return {"type": "italic"}

class bold(el):
    def to_json(self, doc) -> Dict[str, Any]:
        return {"type": "bold"}


class vertAlign(el):
    def to_json(self, doc) -> Dict[str, Any]:
        # 获取 w:val 属性的值
        val = self.fragment.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
        if val == "baseline":
            return None

        return {"type": val}


class strike(el):
    def to_json(self, doc) -> Dict[str, Any]:
        # 获取 w:val 属性的值
        val = self.fragment.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val")

        if val == '0':
            return None

        return {"type": "strike"}

class colorConvertor:
    def is_hex_color(self, value):
        """检查是否是有效的十六进制颜色值，不带 # 的情况"""
        return re.match(r'^([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})$', value) is not None

    def convert_to_hex(self, value):
        """将颜色名称或无 # 的十六进制值转换为带 # 的十六进制颜色值"""
        if self.is_hex_color(value):
            return f'#{value}'

        # 否则，尝试将其作为颜色名称处理
        try:
            return webcolors.name_to_hex(value)
        except ValueError:
            return None

class highlight(el, colorConvertor):
    # 背景色
    def to_json(self, doc) -> Dict[str, Any]:
        # 获取 w:val 属性的值
        val = self.fragment.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
        if not val:
            return None

        val = self.convert_to_hex(val)

        return {"type": "highlight", "attrs": {"color": val}}

class textStyle(el, colorConvertor):
    # 字体颜色
    def to_json(self, doc) -> Dict[str, Any]:
        # 获取 w:val 属性的值
        val = self.fragment.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
        if not val:
            return None

        val = self.convert_to_hex(val)

        return {"type": "textStyle", "attrs": {"color": val}}



class fldChar(el):
    def to_json(self, doc) -> Dict[str, Any]:
        val = self.fragment.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fldCharType')
        if val is None or val == "separate":
            return None

        return {"type": "link" + val}


class instrText(el):
    def to_json(self, doc) -> Optional[Dict[str, Any]]:
        insrText = self.fragment.text
        url = instrText.extract_url(insrText)
        if url is None:
            return None

        return {"type": "link", "attrs": {"href": url, "target": "_blank", "class": None}}
    def extract_url(text):
        pattern = r'HYPERLINK\s+"([^"]+)"'
        match = re.search(pattern, text)
        if match:
            url = match.group(1)
            return url
        else:
            return None
