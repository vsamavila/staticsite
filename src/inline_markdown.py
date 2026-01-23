import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue

        parts = n.text.split(delimiter)

        if delimiter in n.text and len(parts) % 2 == 0:
            raise Exception("Invalid Markdown syntax: unbalanced delimiters")

        nodes = []

        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                nodes.append(TextNode(part, TextType.TEXT))
            else:
                nodes.append(TextNode(part, text_type))

        new_nodes.extend(nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    print(matches)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    print(matches)
    return matches




