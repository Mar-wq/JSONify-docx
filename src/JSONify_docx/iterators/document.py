from docx.oxml.ns import qn
from ..elements import body
from .generic import register_iterator

register_iterator(
    "doc",
    TAGS_TO_YIELD={qn("w:body"): body},
)
