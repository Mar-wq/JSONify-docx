"""
Utilities for setting options that change how the document is traversed
"""



from ..iterators.generic import register_iterator, build_iterators, build_styleId_mapping


def parse_init(doc):
    build_styleId_mapping(doc)
    build_iterators()




