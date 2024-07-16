from .base import container

class document(container):
    """
    文档主体元素
    """
    __type__ = "doc"

    def to_json(self, doc):

        # 获取第一个元素的 JSON 表示，如果没有元素，则 content 为 None
        first_elt = next(iter(self), None)
        content = first_elt.to_json(doc) if first_elt is not None else None


        return content
