import glob
import javalang
import base64
import streamlit as st
import class_parser
import interface_parser
import sys

from IPython.display import Image, display
import matplotlib.pyplot as plt

def convert_to_mermaid(java_code):
    tree = javalang.parse.parse(java_code)
    # check if it is an interface or a class
    if tree.types[0].__class__.__name__ == "InterfaceDeclaration":
      return interface_parser.interface_convert_to_mermaid(java_code)
    else:
      return class_parser.class_convert_to_mermaid(java_code)

# read from folder
folder = sys.argv[1] if len(sys.argv) > 1 else "java_codes"
# read from that folder
import os
java_codes = []
selected = []
with st.sidebar:
  for filename in glob.iglob(folder + '/**/*.java', recursive=True):
      basename = os.path.splitext(os.path.basename(filename))[0]
      if filename.endswith(".java"):
          selected.append(st.checkbox(basename))
          with open(os.path.join(folder, filename), "r") as f:
              java_codes.append(f.read())

mermaid_diagram = "classDiagram\n"
for i in range(len(selected)):
    if selected[i]:
        mermaid_diagram += convert_to_mermaid(java_codes[i].replace("\"\"\"", "\"").replace("\n", ""))
graphbytes = mermaid_diagram.encode("ascii")
base64_bytes = base64.b64encode(graphbytes)
base64_string = base64_bytes.decode("ascii")

# print('https://mermaid.ink/img/' + base64_string)

image = Image(url = 'https://mermaid.ink/img/' + base64_string)
st.write(image)
