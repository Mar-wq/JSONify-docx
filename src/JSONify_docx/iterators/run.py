from docx.oxml.ns import qn

from JSONify_docx.elements.image import image
from JSONify_docx.elements.math import math, embObject
from JSONify_docx.elements.run import rPr, underline, italic, bold, text, vertAlign, strike, highlight, textStyle, \
    fldChar, instrText
from JSONify_docx.iterators.generic import register_iterator

register_iterator("run",
                  TAGS_TO_YIELD={
                      qn("w:drawing"): image,
                      qn("m:oMath"): math,
                      #qn("w:object"): embObject,
                      qn("w:rPr"): rPr,
                      qn("w:t"): text,
                      qn("w:fldChar"): fldChar,
                      qn("w:instrText"): instrText
                  }
                  )


register_iterator("rPr",
                  TAGS_TO_YIELD={
                      qn("w:u"): underline,
                      qn("w:i"): italic,
                      qn("w:b"): bold,
                      qn("w:vertAlign"): vertAlign,
                      qn("w:strike"): strike,
                      qn("w:highlight"): highlight,
                      qn("w:color"): textStyle,
                  }
                  )
