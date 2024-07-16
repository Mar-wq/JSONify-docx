from typing import Dict, Any

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
        iter_me = peekable(self)  # 可用于在不消耗迭代器的情况下查看当前迭代对象
        for elt in iter_me:
            JSON = elt.to_json(doc)

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