from ..types import xmlFragment
from docx.enum.style import WD_STYLE_TYPE
from typing import (
        Optional,
        Type,
        Dict,
        NamedTuple,
        NewType,
        Callable,
        Generator,
        List
)
from ..elements.base import el



FragmentIterator = NewType('FragmentIterator',
        Callable[[xmlFragment, Optional[str]], Generator[xmlFragment, None, None]])




FragmentIterator = NewType('FragmentIterator',
        Callable[[xmlFragment, Optional[str]], Generator[xmlFragment, None, None]])


class ElementHandlers(NamedTuple):
    """
    A convenience class
    """
    TAGS_TO_YIELD: Optional[Dict[str, Type[el]]]


ElementHandlers.__new__.__defaults__ = (None,)* 1


__definitions__: Dict[str, ElementHandlers] = {}
__built__: Dict[str, ElementHandlers] = {}
__styles__: Dict[str, WD_STYLE_TYPE.PARAGRAPH] = {}
#  todo 用于将word内容的字体隐射到编辑器内
__fontFamily__: Dict[str, str] = {}


def register_iterator(name: str,
                      TAGS_TO_YIELD: Dict[str, Type[el]] = None
                     ) -> None:
    """
        一个带有特定约定的迭代器，只会迭代所需要的资源。
    """


    __definitions__[name] = ElementHandlers(
            TAGS_TO_YIELD
            )




def build_styleId_mapping(doc):
    styles = doc.styles

    # 创建样式ID到样式对象的映射字典

    for style in styles:
        if style.type == 1:  # 1 表示段落样式
            __styles__[style.style_id] = style



def build_iterators() -> None:
    """
    Build the iterators for the current iteration
    """

    _resovled: List[str] = []
    def _resolve(x: str):

        if x in _resovled:
            return

        xdef = __definitions__[x]


        TAGS_TO_YIELD = dict(xdef.TAGS_TO_YIELD) if xdef.TAGS_TO_YIELD else {}




        __built__[x] = ElementHandlers(
                TAGS_TO_YIELD=TAGS_TO_YIELD,
                )

        _resovled.append(x)

    for name in __definitions__:
        _resolve(name)




def xml_iter(
        p: xmlFragment,
        name: str,            #表示处理器的名称。
        msg: Optional[str] = None) -> Generator[el, None, None]:
    """
    遍历需要的元素的XML节点(el)。
    """

    handlers = __built__[name]

    children = p.getchildren()
    if not children:
        return

    current: Optional[xmlFragment] = p.getchildren()[0]


    while current is not None:

        if handlers.TAGS_TO_YIELD \
                and current.tag in handlers.TAGS_TO_YIELD:

            yield handlers.TAGS_TO_YIELD[current.tag](current)

        #移动到下一个兄弟节点
        current = current.getnext()

    return