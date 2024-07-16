"""
遍历容器
"""
from docx.oxml.ns import qn
from .generic import register_iterator
from ..elements.paragraph import paragraph
from ..elements.table import table


register_iterator(
    "body", TAGS_TO_YIELD={
        qn("w:p"): paragraph,
        qn("w:tbl"): table
    }
)
