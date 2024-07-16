from docx.oxml.ns import qn

from JSONify_docx.elements.paragraph import paragraph
from JSONify_docx.elements.table import tr, tc, table
from JSONify_docx.iterators.generic import register_iterator


register_iterator("table", TAGS_TO_YIELD={qn("w:tr"):tr})
register_iterator("tableRow", TAGS_TO_YIELD={qn("w:tc"):tc})
register_iterator("tableCell", TAGS_TO_YIELD={qn("w:p"): paragraph, qn("w:tbl"): table})