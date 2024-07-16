from lxml import etree

from ..iterators.generic import __styles__
def get_paragraph_format_through_styleId(paragraph):
    # 将 CT_P 对象转换为 XML 字符串
    xml_string = etree.tostring(paragraph, encoding='unicode')

    # 解析 XML 字符串为 lxml 元素
    xml_element = etree.fromstring(xml_string)
    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # 获取段落样式ID
    style_id = xml_element.xpath('.//w:pPr//w:pStyle/@w:val', namespaces=namespaces)
    if not style_id:
        return None
    style_id = style_id[0]

    # 获取样式对象
    style = __styles__.get(style_id)
    if not style:
        return None

        # 获取对齐方式
    alignment_mapping = {
        0: 'left',
        1: 'center',
        2: 'right',
        3: 'justify',
    }
    alignment = None
    if style.paragraph_format.alignment:
        alignment = alignment_mapping.get(style.paragraph_format.alignment, 'left')

    # 获取字体大小，加粗，斜体等属性
    format_dict = {}

    if alignment:
        format_dict['alignment'] = alignment
    if style.font.size:
        format_dict['font_size'] = style.font.size.pt  # 转换为磅值
    if style.font.bold is not None:
        format_dict['bold'] = style.font.bold
    if style.font.italic is not None:
        format_dict['italic'] = style.font.italic

    return format_dict




