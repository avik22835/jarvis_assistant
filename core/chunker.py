import os
import json
from tree_sitter_language_pack import get_parser

CHUNK_NODE_TYPES = {
    "function_definition", #method
    "function_declaration",#method
    "method_definition",#method
    "method_declaration",#method
    "arrow_function",#method
    "generator_function_declaration",#method
    "function_expression",#method
    "function_item",#method
    "impl_item",#class
    "class_declaration",#class
    "class_definition",#class
    "constructor_declaration",#method
    "class_specifier",#class
    "field_declaration",#class
    "struct_item",#class
    "enum_item",#class
    "trait_item",#class
    "defn", "defnDef",#method
    "jsx_element",#special
    "jsx_fragment",#special
    "component_declaration",#class
    "element", "start_tag", "script_element", "style_element",#special
    "rule_set", "at_rule", "style_rule", "media_rule",#special
    "namespace_definition",#class
    "interface_declaration",#class
}


LANGUAGES = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "javascript",      # React JSX
    ".tsx": "typescript",      # React TypeScript
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".cpp": "cpp",
    ".c": "c",
    ".html": "html",
    ".css": "css",
    ".scss": "css",            # SCSS can still be parsed as CSS if needed
    ".php": "php",
    ".json": "json",
    ".xml": "xml",
    ".vue": "vue",
    ".h": "c",
    ".hpp": "cpp",
}

SPECIAL_CHUNK_TYPES = {
    "jsx_element",
    "jsx_fragment",
    "element",
    "start_tag",
    "script_element",
    "style_element",
    "rule_set",
    "at_rule",
    "style_rule",
    "media_rule"
}

CLASS_NODES = {
    "class_definition",     # Python
    "class_declaration",    # Java, JS/TS, PHP
    "class_specifier",      # C++
    "struct_item", "impl_item", "enum_item",  # Rust
    "interface_declaration",  # TypeScript
    "trait_item",
    "namespace_definition"
}

METHOD_NODES = {
    "function_definition",     # Python, C
    "function_declaration",    # JS, Go
    "method_definition",       # JS, Rust
    "method_declaration",      # Java, Go
    "arrow_function",          # JS/TS
    "function_item",           # Rust
    "defn", "defnDef",         # Scala
    "generator_function_declaration",
    "function_expression",
    "constructor_declaration"
}

PARSERS = {ext: get_parser(lang) for ext, lang in LANGUAGES.items()}

def read_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
    

def extract_chunks(file_path, content):
    ext = os.path.splitext(file_path)[1]
    if ext not in PARSERS:
        return []


    parser = PARSERS[ext]
    tree = parser.parse(bytes(content, "utf-8"))
    root = tree.root_node

    chunks = []

    for node in root.children:
        # Top-level method/function
        if node.type in METHOD_NODES:
            chunks.append(make_chunk(node, file_path, ext))

        # Class-like structures
        elif node.type in CLASS_NODES:
            class_name = get_node_name(node)
            has_methods = False

            for child in node.named_children:
                if child.type in METHOD_NODES:
                    has_methods = True
                    chunk = make_chunk(child, file_path, ext)
                    chunk["class"] = class_name
                    chunks.append(chunk)

            if not has_methods and node.end_byte - node.start_byte > 5:
                chunk = make_chunk(node, file_path, ext)
                chunk["chunk_type"] = "full_class"
                chunks.append(chunk)
        
        elif node.type in SPECIAL_CHUNK_TYPES:
            chunk = make_chunk(node, file_path, ext)
            chunk["chunk_type"] = "special"
            chunks.append(chunk)

    return chunks


def get_node_name(node):
    name_node = node.child_by_field_name("name")
    return name_node.text.decode() if name_node else "anonymous"


def make_chunk(node, file_path, ext):
    return {
        "file": file_path,
        "lang": ext,
        "type": node.type,
        "name": get_node_name(node),
        "code": node.text.decode(),
        "start_line": node.start_point[0] + 1,
        "end_line": node.end_point[1] + 1,
    }   


def get_project_context(repo_path):
    readme_files = ["README.md", "readme.md"]
    for file_name in readme_files:
        path = os.path.join(repo_path, file_name)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
            
    # If no README found
    print("❓ README.md not found.")
    print("Please enter a short description of your project:")
    return input("> ")


