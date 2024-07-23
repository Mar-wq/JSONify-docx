from __future__ import annotations
from typing import Optional, Dict, Sequence

class xmlFragment:
    """一个抽象类，表示python-docx返回的XML片段
    """
    def getchildren(self) -> Sequence[xmlFragment]:
        ...
    def getparent(self) -> Optional[xmlFragment]:
        ...
    def getnext(self) -> Optional[xmlFragment]:
        ...
    def xpath(self, x:str) -> Optional[xmlFragment]: #根据 XPath 表达式查找元素。返回类型是 Optional[xmlFragment]，表示返回值可以是 xmlFragment 类型或 None。
        ...

    def get(self, param):
        ...

