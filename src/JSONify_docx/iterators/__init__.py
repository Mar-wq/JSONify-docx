"""
Docx 迭代器
"""

from .generic import xml_iter

# 迭代器定义:
import importlib
importlib.import_module(".document",__package__)
importlib.import_module(".body",__package__)
importlib.import_module(".paragraph",__package__)
importlib.import_module(".run",__package__)
importlib.import_module(".table",__package__)