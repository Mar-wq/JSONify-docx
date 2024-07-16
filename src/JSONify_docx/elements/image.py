import base64
import logging
from typing import Dict, Any

from docx import Document, ImagePart
from docx.oxml.ns import qn
from JSONify_docx.elements import el


from docx.image.image import Image
from docx.parts.image import ImagePart

from PIL import Image
from io import BytesIO




class image(el):
    """
    A Text element
    """

    __type__ = "piture"



    def __init__(self, x):
        super().__init__(x)
        # 获取软连接的信息
        img = x.xpath('.//pic:pic')[0]
        self.embed = img.xpath('.//a:blip/@r:embed')[0]
        self.out = {}
        self.out['type'] = 'image'
        self.out['attrs'] = self.get_image_properties(x)


    def to_json(self, doc) -> Dict[str, Any]:

        #通过软连接直接拿到图片数据
        related_part: ImagePart = doc.part.related_parts[self.embed]
        image: Image = related_part.image
        # 后缀
        ext = image.ext

        # 二进制内容
        blob = image.blob

        sz = len(blob)
        base64_data = base64.b64encode(blob).decode('utf-8')
        self.out["attrs"]['blob'] = base64_data
        self.out['attrs']['ext'] = ext
        self.out['attrs']['sz'] = sz
        return self.out

    def get_image_properties(self, drawing_element):
        properties = {
            "blob": None,
            "alt": None,
            "title": None,
            "lockAspectRatio": True,
            "width": None,
            "height": None,
            "display": "inline",
            "chapter": "N",
            "describe": "N"
        }

        try:
            # 获取嵌入的图片属性
            blip = drawing_element.xpath('.//a:blip')[0]
            embed = blip.get(qn('r:embed'))

            # 获取其他属性
            alt_text = drawing_element.xpath('.//wp:docPr/@descr')
            title_text = drawing_element.xpath('.//wp:docPr/@title')
            properties["alt"] = alt_text[0] if alt_text else None
            properties["title"] = title_text[0] if title_text else None

            # 获取图片的尺寸信息
            ext = drawing_element.xpath('.//a:ext')[0]
            cx = int(ext.get('cx'))  # 宽度，单位是EMU（英制单位）
            cy = int(ext.get('cy'))  # 高度，单位是EMU（英制单位）

            # 将EMU转换为英寸或其他单位（1英寸 = 914400 EMU）
            width_inches = cx / 914400
            height_inches = cy / 914400

            # 更新属性字典
            properties["width"] = width_inches
            properties["height"] = height_inches



            # 锁定宽高比
            lock_aspect_ratio = drawing_element.xpath('.//a:prstGeom/@prst')
            properties["lockAspectRatio"] = lock_aspect_ratio[0] == 'rect' if lock_aspect_ratio else True
        except Exception as e:  # 捕获所有Exception基类的异常
            logging.error("An error occurred while processing the image attrs: %s", str(e))


        return properties