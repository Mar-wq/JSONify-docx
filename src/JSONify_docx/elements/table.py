from typing import Dict, Any

from more_itertools import peekable

from JSONify_docx.elements import container


class table(container):
    __type__ = "table"


    def __init__(self, x):
        super().__init__(x)
        self.out = {"type": self.__type__, "attrs":{}}

    def to_json(self, doc) -> Dict[str, Any]:
        """Coerce a container object to JSON
        """

        content = []
        iter_me = peekable(self)   #可用于在不消耗迭代器的情况下查看当前迭代对象
        for elt in iter_me:
            JSON = elt.to_json(doc)

            content.append(JSON)

        self.out['content'] = content

        return self.out



class tr(container):
    __type__ = "tableRow"

    def __init__(self, x):
        super().__init__(x)
        self.out = {"type": self.__type__, "attrs": {}}

    def to_json(self, doc) -> Dict[str, Any]:
        """Coerce a container object to JSON
        """

        content = []
        iter_me = peekable(self)  # 可用于在不消耗迭代器的情况下查看当前迭代对象
        for elt in iter_me:
            JSON = elt.to_json(doc)

            content.append(JSON)

        self.out['content'] = content

        return self.out


class tc(container):
    __type__ = "tableCell"

    def __init__(self, x):
        super().__init__(x)
        self.out = {"type": self.__type__, "attrs": {}}

    def to_json(self, doc) -> Dict[str, Any]:
        """Coerce a container object to JSON
        """

        content = []
        iter_me = peekable(self)  # 可用于在不消耗迭代器的情况下查看当前迭代对象
        for elt in iter_me:
            JSON = elt.to_json(doc)

            content.append(JSON)

        self.out['content'] = content

        return self.out