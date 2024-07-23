from typing import Optional, Dict, Any,  Generator


from ..types import xmlFragment



class el:
    """
    docx元素的抽象基类
    """
    __type__: str
    fragment: xmlFragment

    def __init__(self, x: xmlFragment):
        self.fragment = x

    def to_json(self, doc):
        ...


class container(el):
    """
    表示可以包含其他元素对象的对象
    """

    def __iter__(self) -> Generator['el', None, None]:
        from ..iterators import xml_iter
        node: xmlFragment = self.fragment
        for elt in xml_iter(node, self.__type__):
            yield elt
