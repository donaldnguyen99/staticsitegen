import os, re, shutil
from enum import Enum
from typing import List

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode

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
    if re.match("^#{1,6} .+$", block):
        return "heading"
    elif block.startswith("```\n") and block.endswith("\n```"):
        return "code"
    elif len(re.findall("^>|\n>", block)) == len(block.splitlines()):
        return "quote"
    elif block and block[0] in "*-" and is_unordered_list:
        return "unordered_list"
    elif re.findall("^(\d+)\. ", block, re.MULTILINE) == list(map(str, range(1, len(block.splitlines()) + 1))):
        return "ordered_list"
    else:
        return "paragraph"

def text_to_children(text: str):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def block_to_heading_html_node(markdown: str):
    res = re.match("^(#{1,6}) (.+)$", markdown)
    heading_markers = res.group(1)
    if heading_markers:
        inline_heading = res.group(2)
        return ParentNode(f"h{len(res.group(1))}", text_to_children(inline_heading))
    else:
        raise ValueError("Not a valid markdown heading.")

def block_to_code_html_node(markdown: str):
    # code block cannot be delimited inline so it is a leaf node
    child = text_node_to_html_node(TextNode(markdown[3:-3].strip(), TextType.CODE))
    return ParentNode("pre", [child])

def block_to_quote_html_node(markdown: str):
    # Assuming no nested blockquotes
    text = "\n".join([line.strip(">").strip() for line in markdown.splitlines()])
    return ParentNode("blockquote", text_to_children(text))

def block_to_unordered_list_html_node(markdown: str):
    # Assuming no nested lists
    lines = markdown.splitlines()
    bullet = markdown[0]
    items = [line.strip().removeprefix(bullet + " ") for line in lines]
    
    item_html_nodes = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ul", item_html_nodes)

def block_to_ordered_list_html_node(markdown: str):
    lines = markdown.splitlines()
    items = [line.strip().removeprefix(str(num) + ". ") for num, line in enumerate(lines, 1)]
    
    item_html_nodes = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ol", item_html_nodes)

def block_to_paragraph_html_node(markdown: str):
    return ParentNode("p", text_to_children(markdown))

def markdown_to_html_node(markdown: str):
    markdown_blocks = markdown_to_blocks(markdown)
    block_to_html_node_funcs = {
        "heading": block_to_heading_html_node,
        "code": block_to_code_html_node,
        "quote": block_to_quote_html_node,
        "unordered_list": block_to_unordered_list_html_node,
        "ordered_list": block_to_ordered_list_html_node,
        "paragraph": block_to_paragraph_html_node,
    }

    leaf_nodes = []
    for markdown_block in markdown_blocks:
        block_type = block_to_block_type(markdown_block)
        leaf_nodes.append(block_to_html_node_funcs[block_type](markdown_block))
    return ParentNode("div", leaf_nodes)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == "heading" and block.startswith("# "):
            return block[2:].strip()
    raise Exception("A title cannot be found")

