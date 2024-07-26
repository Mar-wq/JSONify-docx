from typing import Dict, Any

from docx.oxml.ns import qn
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

        for elt in self:
            JSON = elt.to_json(doc)

            content.append(JSON)

        content = self.handle_link(content)
        content = self.merge_content(content)
        self.out["content"] = content

        return self.out

    #处理超链接
    def handle_link(self, content):
        new_content = []
        len1 = len(content)
        i = 0
        while i < len1:
            j = i
            while j < len1 and content[j].get("type") != "linkbegin":
                new_content.append(content[j])
                j += 1
            if j >= len1:
                break
            link = None
            while j < len1 and content[j].get("type") != "linkend":
                if content[j].get("type") == 'link':
                    if "marks" in content[j]:
                        del content[j]["marks"]
                    link = content[j]
                elif content[j].get("type") == 'text':
                    if "marks" not in content[j]:
                        content[j]["marks"] = []
                    content[j]["marks"].append(link)

                    new_content.append(content[j])
                j += 1
            i = j + 1
        return new_content


    # 合并自定义masks相同且类型为text的run块
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
        """
        :param content: run的列表
        :param i:    下标i
        :param j:    下标j
        :return:     返回两个marks标签是否相同
        """
        marks1 = content[i].get('marks', [])
        marks2 = content[j].get('marks', [])


        # 过滤掉 None 元素，避免不必要的异常
        marks1 = [mark for mark in marks1 if mark is not None]
        marks2 = [mark for mark in marks2 if mark is not None]


        # 如果两个元素都没有 marks，则认为相同
        if not marks1 and not marks2:
            return True

        if not marks1 or not marks2:
            return False


        # 对 marks 列表进行排序
        sorted_marks1 = sorted(marks1, key=lambda x: x['type'])
        sorted_marks2 = sorted(marks2, key=lambda x: x['type'])

        return sorted_marks1 == sorted_marks2


    def has_text_attribute(self, run):
        return 'text' in run

    def has_inherited_style(self, p_element):
        """
        处理继承段落样式，通过标签判断是否继承样式
        :param p_element: 段落对应的element对象
        :return:
        """

        pPr = p_element.find(qn("w:pPr"))

        if pPr is not None:
            # 查找段落样式<w:pStyle>标签
            pStyle = pPr.find(qn("w:pStyle"))
            if pStyle is not None:
                return True
        return False

    def handle_inherited_style(self, x):
        """
        获取段落的继承样式属性
        :param x:
        :return:
        """
        # 初始化属性
        pf = None
        text_align = "left"
        line_height = 1
        style_id = x.style
        style =  __styles__[style_id]


        # get paragraph format
        text_val = None
        if style is not None:
            pf = style.paragraph_format
        if pf:
            if hasattr(pf, 'alignment'):
                if pf.alignment:
                    text_val = pf.alignment.name.lower()

                if hasattr(pf, 'line_spacing'):
                    line_height_val = pf.line_spacing
                    if line_height_val is not None:
                        line_height_val = int(line_height_val) / 240  # 转换为标准行高（1.0为240）

                        if line_height_val < 1:
                            line_height = 1
                        else:
                            line_height = paragraph.round_to_nearest_half(line_height_val)

        # 其他对齐方式按左对齐处理
        if text_val is not None:
            if text_val == 'center':
                text_align = 'center'
            elif text_val == 'right':
                text_align = 'right'
            elif text_val == 'both':
                text_align = 'justify'



        indent = pf.first_line_indent


        # 为确保解析服务的正常，使用了其他预设样式统一作为普通正文样式进行处理
        if not style_id.isdigit() or int(style_id) > 6:
            return {
                "type": "paragraph",
                "attrs": {
                    "textAlign": text_align,
                    "indent": indent,
                    "lineHeight": line_height,
                }
            }



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
        line_height = 1

        # 一个字符的高度约等于字体大小
        font_size = 18  # 按照新编辑器内的默认字体大小设置
        twip_per_char = 240  # 每个字符对应的twip数，默认240

        # 获取命名空间
        nsmap = p_element.nsmap

        # 查找段落属性<w:pPr>标签
        pPr = p_element.find(qn("w:pPr"))

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
            p_indent = pPr.find(qn("w:ind"))
            if p_indent is not None:
                left_indent = p_indent.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left')
                if left_indent is not None:
                    indent_twip = int(left_indent)
                    indent = indent_twip / twip_per_char
                    indent = paragraph.round_to_nearest_even(indent)

            # 获取行距
            p_spacing = pPr.find(qn("w:spacing"))
            if p_spacing is not None:
                line_height_val = p_spacing.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}line')
                if line_height_val is not None:
                    line_height_val = int(line_height_val) / 240  # 转换为标准行高（1.0为240）

                    if line_height_val < 1:
                        line_height = 1
                    else:
                        line_height = paragraph.round_to_nearest_half(line_height_val)

        return {
            "type": "paragraph",
            "attrs": {
                "textAlign": text_align,
                "indent": indent,
                "lineHeight": line_height
            }
        }

    def round_to_nearest_half(number):
        return round(number * 2) / 2

    def round_to_nearest_even(value):
        """
        返回：
        rounded_value -- 四舍五入后的偶数值
        """
        return int(round(value / 2.0) * 2)


class commentRangeStart(el):
    __type__ = "commentRangeStart"


class commentRangeEnd(el):
    __type__ = "commentRangeEnd"


class pPr(container):
    __type__ = "pPr"


class pStyle(el):
    pass
