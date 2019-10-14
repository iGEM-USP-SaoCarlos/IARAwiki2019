from iGEMconf import TEMPLATES_DIR, PAGES_DIR, COMPILED_DIR
import re


def compile_path(path):
    name = path.name
    outpath = COMPILED_DIR/name
    if path.exists():

