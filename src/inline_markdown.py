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


def split_nodes_image(old_nodes):
    new_nodes = []

    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue
         
        images = extract_markdown_images(n.text)

        if len(images) == 0:
             new_nodes.append(n)
             continue

        remaining = n.text

        for alt, url in images:
            chunk = f"![{alt}]({url})"
            parts = remaining.split(chunk, 1)
            if parts[0] !="":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining = parts[1]

        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue
         
        links = extract_markdown_links(n.text)

        if len(links) == 0:
             new_nodes.append(n)
             continue

        remaining = n.text

        for text, url in links:
            chunk = f"[{text}]({url})"
            parts = remaining.split(chunk, 1)
            if parts[0] !="":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url)) 
            remaining = parts[1]

        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []

    for n in blocks:
        n = n.strip()
        if n != "":
            clean_blocks.append(n)
    return clean_blocks











def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    print(matches)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    print(matches)
    return matches




