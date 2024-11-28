import re

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
            

def extract_markdown_images(text):
    pattern = re.compile("!\[(.*?)\]\((.*?)\)")
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = re.compile("\[(.*?)\]\((.*?)\)")
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    # new_nodes = []

    # old_node: TextNode
    # for old_node in old_nodes:
    #     if old_node.text_type != TextType.TEXT:
    #         new_nodes.append(old_node)
    #         continue

    #     images = extract_markdown_images(old_node.text)
    #     split_text = [old_node.text]
    #     last_text = old_node.text
    #     for alt_text, url in images:
    #         split_text = last_text.split(f"![{alt_text}]({url})", 1)
    #         if split_text[0] != "":
    #             new_nodes.append(TextNode(split_text[0], TextType.TEXT))
    #         new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
    #         if split_text[-1] != "":
    #             last_text = split_text[-1]
    #     if split_text[-1] != "":
    #         new_nodes.append(TextNode(split_text[-1], TextType.TEXT))
    # return new_nodes
    return split_nodes_link_helper(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes_link_helper(old_nodes, TextType.LINK)

def split_nodes_link_helper(old_nodes, text_type: TextType = TextType.LINK):
    if text_type not in [TextType.LINK, TextType.IMAGE]:
        raise ValueError("Only TextType.LINK and TextType.IMAGE is accepted for text_type arg")
    start_text = "!" if text_type == TextType.IMAGE else ""
    func = extract_markdown_images if text_type == TextType.IMAGE else extract_markdown_links
    new_nodes = []

    old_node: TextNode
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        link = func(old_node.text)
        split_text = [old_node.text]
        last_text = old_node.text
        for alt_text, url in link:
            split_text = last_text.split(start_text + f"[{alt_text}]({url})", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, text_type, url))
            if split_text[-1] != "":
                last_text = split_text[-1]
        if split_text[-1] != "":
            new_nodes.append(TextNode(split_text[-1], TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    old_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_link(split_nodes_image([old_node]))
    
    delimiters = [
        ("**", TextType.BOLD),
        ("*", TextType.ITALIC),
        ("`", TextType.CODE)
    ]

    for delimiter_str, text_type in delimiters:
        new_nodes = split_nodes_delimiter(new_nodes, delimiter_str, text_type)
    
    return new_nodes

def markdown_to_blocks(markdown: str):
    return list(filter(lambda x: x != "", map(lambda x: x.strip(), markdown.split("\n\n"))))
    
def block_to_block_type(block: str):
    unordered_list_bullet = "\*" if  (block and block[0] in "*-" and block[0] == "*") else "-"

    is_unordered_list = False
    if block and block[0] in "*-":
        is_unordered_list = len(re.findall(f"^{unordered_list_bullet} ", block, re.MULTILINE)) == len(block.splitlines())
    if re.match("^#{1,6} .*?$", block):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif len(re.findall("^>|\n>", block)) == len(block.splitlines()):
        return "quote"
    elif block and block[0] in "*-" and is_unordered_list:
        return "unordered_list"
    elif re.findall("^(\d+)\. ", block, re.MULTILINE) == list(map(str, range(1, len(block.splitlines()) + 1))):
        return "ordered_list"
    else:
        return "paragraph"