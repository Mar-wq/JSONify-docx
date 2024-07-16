from JSONify_docx.elements.math import math, mathParagraph
from JSONify_docx.elements.run import run
from JSONify_docx.iterators.generic import register_iterator
from docx.oxml.ns import qn

register_iterator("paragraph", TAGS_TO_YIELD={
    qn("w:r"):run,
    qn("m:oMath"):math,
    qn("m:oMathPara"):mathParagraph,
})
