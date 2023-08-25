import javalang

def interface_convert_to_mermaid(java_code):
    tree = javalang.parse.parse(java_code)
    class_diagram = ""

    for path, node in tree.filter(javalang.tree.InterfaceDeclaration):
        class_name = node.name
        extends_clause = node.extends.name if node.extends else ""
        implements_clause = ""

        # Generate the extends and implements clauses
        if extends_clause:
            class_diagram += f"    {class_name} <|-- {extends_clause}\n"
        if implements_clause:
            implements_list = [f"{class_name} <|.. {imp}" for imp in implements_clause.split(",")]
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
            parameters = ", ".join([f"{param.type.name} {param.name}" for param in method.parameters])
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
