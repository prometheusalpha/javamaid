import glob
import javalang
import base64
import streamlit as st
import class_parser
import interface_parser
import sys
import pyperclip
import os
from IPython.display import Image


def get_selected_classes(folder):
    java_codes = []
    with st.sidebar:
        for filename in glob.iglob(folder + "/**/*.java", recursive=True):
            basename = os.path.splitext(os.path.basename(filename))[0]
            if st.checkbox(basename, key=basename):
                with open(os.path.join(folder, filename), "r") as f:
                    java_codes.append({"name": filename, "code": f.read()})
    return java_codes


def parse(java_codes):
    mermaid_diagram = "classDiagram\n  direction LR\n"
    for java_module in java_codes:
        mermaid_diagram += convert_to_mermaid(
            java_module["code"].replace('"""', '"').replace("\n", ""), java_codes
        )
    return mermaid_diagram


def encode(mermaid_diagram):
    graphbytes = mermaid_diagram.encode("ascii")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


def convert_to_mermaid(java_code, selected):
    type = get_type(java_code)
    return convert_to_mermaid_based_on_type(type, java_code, selected)


def get_type(java_code):
    if java_code.find("record") != -1:
        java_code = class_parser.change_record_to_class(java_code)
    tree = javalang.parse.parse(java_code)
    return tree.types[0].__class__.__name__


def convert_to_mermaid_based_on_type(type, java_code, selected):
    if type == "InterfaceDeclaration":
        return interface_parser.interface_convert_to_mermaid(java_code, selected)
    else:
        return class_parser.class_convert_to_mermaid(java_code, selected)


folder = sys.argv[1] if len(sys.argv) > 1 else ""
java_codes = get_selected_classes(folder)
mermaid_diagram = parse(java_codes)
base64_string = encode(mermaid_diagram)

# button to copy the mermaid diagram to clipboard
if st.button("Copy mermaid code to clipboard", type="primary"):
    pyperclip.copy(mermaid_diagram)

image = Image(url="https://mermaid.ink/img/" + base64_string)
st.write(image)
