



__version__ = "1.0"

__author__ = "<hdy>"

__email__ = "<977648857@qq.com>"


from .elements import document
from .iterators.generic import build_iterators
from .utils.set_options import parse_init


# --------------------------------------------------
# Main API
# --------------------------------------------------
def doc_JSONify(doc):
    parse_init(doc)
    return document(doc.element).to_json(doc)