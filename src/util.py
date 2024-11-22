from typing import List

from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("TextNode does not have a valid text type.")


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []

    old_node: TextNode
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # See if any text type TextNodes can be split into multiple nodes
        if old_node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Invalid markdown: missing a closing delimiter ({delimiter}).")
        delimited_text = old_node.text.split(delimiter)
        
        is_text = True
        delimited_textnodes = []
        for text in delimited_text:
            if text != "":
                delimited_textnodes.append(TextNode(text, TextType.TEXT if is_text else text_type))
            is_text = not is_text
        
        new_nodes.extend(delimited_textnodes)

    return new_nodes
            



