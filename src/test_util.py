import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from util import text_node_to_html_node, split_nodes_delimiter

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("hello world", TextType.TEXT)
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), 
            "hello world"
        )

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("hello world", TextType.CODE)
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), 
            "<code>hello world</code>"
        )

    def test_text_node_to_html_node_url(self):
        text_node = TextNode("hello world", TextType.LINK, "https://www.google.com")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), 
            "<a href=\"https://www.google.com\">hello world</a>"
        )
    
    def test_text_node_to_html_node_image(self):
        text_node = TextNode("hello world", TextType.IMAGE, "https://www.google.com")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), 
            "<img src=\"https://www.google.com\" alt=\"hello world\"></img>"
        )


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_nodes_delimiter_code_in_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )
    
    def test_split_nodes_delimiter_bold_in_text(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_italic_in_text(self):
        node = TextNode("This is text with a *italic block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ]
        )
    
    def test_split_nodes_delimiter_code_missing_close(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception):
            node = TextNode("This is text with a `code block word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        

if __name__ == "__main__":
    unittest.main()