from tree_sitter_language_pack import get_parser

parser = get_parser("python")
tree = parser.parse(b"def hello(): pass")
root = tree.root_node

def print_node(node, indent=0):
    print("  " * indent + f"{node.type} [{node.start_point} - {node.end_point}]")
    for child in node.children:
        print_node(child, indent + 1)

print_node(root)

