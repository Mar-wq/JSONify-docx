from typing import Dict, Any

from more_itertools import peekable

from . import el, container
from ..iterators.generic import __styles__


class paragraph(container):
    """ 
    Represents a simple paragraph
    """

    __type__ = "paragraph"

    def __init__(self, x):
        super().__init__(x)
        if self.has_inherited_style(x):
            self.out = self.handle_inherited_style(x)
        else:
            self.out = self.handle_style(x)

    def to_json(self, doc) -> Dict[str, Any]:

        content = []

        iter_me = peekable(self)  # 可用于在不消耗迭代器的情况下查看当前迭代对象
        for elt in iter_me:
            JSON = elt.to_json(doc)

            content.append(JSON)

        content = self.merge_content(content)
        self.out["content"] = content

        return self.out

    # 合并自定义masks相同的run块
    def merge_content(self, content):
        filtered_content = [item for item in content if item.get("type") is not None]
        merged_content = []
        i = 0
        len1 = len(filtered_content)

        while i < len1:
            while i < len1 and filtered_content[i]["type"] != "text":
                merged_content.append(filtered_content[i])
                i += 1

            if i >= len1:
                break

            j = i + 1
            while j < len1 and filtered_content[j].get("type") == "text" and self.compare_marks(filtered_content, i, j):
                filtered_content[i]['text'] += filtered_content[j]['text']
                j += 1
            merged_content.append(filtered_content[i])
            i = j

        return merged_content

    def compare_marks(self, content, i, j):
        marks1 = content[i].get('marks', [])
        marks2 = content[j].get('marks', [])

        # 如果两个元素都没有 marks，则认为相同
        if not marks1 and not marks2:
            return True

        # 对 marks 列表进行排序
        sorted_marks1 = sorted(marks1, key=lambda x: x['type'])
        sorted_marks2 = sorted(marks2, key=lambda x: x['type'])

        return sorted_marks1 == sorted_marks2


    def has_text_attribute(self, run):
        return 'text' in run

    def has_inherited_style(self, p_element):

        # 查找段落属性<w:pPr>标签
        pPr = p_element.find('.//w:pPr', namespaces=p_element.nsmap)

        if pPr is not None:
            # 查找段落样式<w:pStyle>标签
            pStyle = pPr.find('.//w:pStyle', namespaces=p_element.nsmap)
            if pStyle is not None:
                return True
        return False

    def handle_inherited_style(self, x):

        # 初始化属性
        text_align = "left"
        indent = 0
        line_height = None
        style_id = x.style
        style =  __styles__[style_id]

        # get paragraph format
        pf = style.paragraph_format
        if hasattr(pf,  'alignment'):
            if pf.alignment:
                text_align = pf.alignment.name.lower()

        #indent =  pf.first_line_indent
        if hasattr(pf, 'line_spacing'):
            line_height = pf.line_spacing



        return {
            "type": "heading",
            "attrs": {
                "textAlign": text_align,
                "indent": indent,
                "lineHeight": line_height,
                "level": int(style_id) - 1
            }
        }

    def handle_style(self, p_element):
        # 初始化属性
        text_align = "left"
        indent = 0
        line_height = None

        # 获取命名空间
        nsmap = p_element.nsmap

        # 查找段落属性<w:pPr>标签
        pPr = p_element.find('.//w:pPr', namespaces=nsmap)

        if pPr is not None:
            # 获取对齐方式
            p_align = pPr.find('.//w:jc', namespaces=nsmap)
            if p_align is not None:
                align_val = p_align.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                if align_val == 'center':
                    text_align = 'center'
                elif align_val == 'right':
                    text_align = 'right'
                elif align_val == 'both':
                    text_align = 'justify'

            # 获取缩进
            p_indent = pPr.find('.//w:ind', namespaces=nsmap)
            if p_indent is not None:
                left_indent = p_indent.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left')
                if left_indent is not None:
                    indent = int(left_indent)

            # 获取行距
            p_spacing = pPr.find('.//w:spacing', namespaces=nsmap)
            if p_spacing is not None:
                line_height_val = p_spacing.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}line')
                if line_height_val is not None:
                    line_height = int(line_height_val) / 240  # 转换为标准行高（1.0为240）

        return {
            "type": "paragraph",
            "attrs": {
                "textAlign": text_align,
                "indent": indent,
                "lineHeight": line_height
            }
        }


class commentRangeStart(el):
    __type__ = "commentRangeStart"


class commentRangeEnd(el):
    __type__ = "commentRangeEnd"


class pPr(container):
    __type__ = "pPr"


class pStyle(el):
    pass
