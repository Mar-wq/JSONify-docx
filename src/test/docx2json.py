from docx import Document

from JSONify_docx import doc_JSONify

doc = Document('./test_section.docx')
json =  doc_JSONify(doc)
print()