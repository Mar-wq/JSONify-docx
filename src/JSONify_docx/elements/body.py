"""
body元素
"""

from more_itertools import peekable
from .base import container


class body(container):
    """
    文档体元素
    """

    __type__ = "body"

    def to_json(self, doc):
        content = []
        iter_me = peekable(self)  # 可用于在不消耗迭代器的情况下查看当前迭代对象
        for elt in iter_me:
            JSON = elt.to_json(doc)

            content.append(JSON)

        # out: Dict[str, Any] = {"TYPE": self.__type__, "VALUE": contents}

        return content
