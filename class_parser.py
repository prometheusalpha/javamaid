import javalang


def class_convert_to_mermaid(java_code, selected):
    if java_code.find("record") != -1:
        java_code = change_record_to_class(java_code)
        print(java_code)

    tree = javalang.parse.parse(java_code)
    class_diagram = ""

    selected_names = []
    for c in selected:
        selected_names.append(c["name"].split("/")[-1].split(".")[0])

    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        class_name = node.name
        extends_clause = node.extends.name if node.extends else ""
        implements_clause = []
        if node.implements:
            implements_clause = [imp.name for imp in node.implements]

        # Generate all the imports from the same java folder
        imports = path[0].imports
        package = path[0].package.name
        for imp in imports:
            import_package = imp.path.split(".")[0]
            import_name = imp.path.split(".")[-1]
            if (
                package.split(".")[0] == import_package
                and not import_name in implements_clause
                and not import_name == extends_clause
            ):
                # add relationship between the class and the imported class
                # only add if the class is selected
                for c in selected_names:
                    if c == import_name:
                        class_diagram += f"    {class_name} --> {import_name}\n"

                    # class_diagram += f"    {class_name} --> {imp.path.split('.')[-1]}\n"

        # Generate the extends and implements clauses

        if extends_clause and selected_names.count(extends_clause) > 0:
            class_diagram += f"    {class_name} --|> {extends_clause}\n"
        if implements_clause:
            selected_imps = [
                imp for imp in implements_clause if selected_names.count(imp) > 0
            ]
            implements_list = [f"{class_name} ..|> {imp}" for imp in selected_imps]
            class_diagram += "    " + "\n    ".join(implements_list) + "\n"

        # Generate the class header
        class_diagram += f"    class {class_name} {{\n"

        # Generate the class fields
        for field in node.fields:
            field_name = field.declarators[0].name
            field_type = field.type.name
            visibility = list(field.modifiers)[0] if field.modifiers else "public"
            if visibility == "private":
                field_name = f"- {field_name}"
            elif visibility == "protected":
                field_name = f"# {field_name}"
            elif visibility == "public":
                field_name = f"+ {field_name}"
            class_diagram += f"    {field_name}: {field_type}\n"

        # Generate the class methods
        for method in node.methods:
            method_name = method.name
            return_type = method.return_type.name if method.return_type else "void"
            parameters = ", ".join(
                [f"{param.type.name} {param.name}" for param in method.parameters]
            )
            visibility = list(method.modifiers)[0] if method.modifiers else "public"
            if visibility == "private":
                method_name = f"- {method_name}"
            elif visibility == "protected":
                method_name = f"# {method_name}"
            elif visibility == "public":
                method_name = f"+ {method_name}"
            class_diagram += f"    {method_name}({parameters}): {return_type}\n"

        class_diagram += "}\n\n"

    return class_diagram

def change_record_to_class(javacode):
  javacode = javacode.replace("record", "class")
  javacode = javacode.replace(",", ";")
  javacode = javacode.replace(")", ";")
  javacode = javacode.replace("{", "")
  javacode = javacode.replace("(", "{")
  return javacode
