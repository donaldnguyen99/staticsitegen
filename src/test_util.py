import unittest

from textnode import TextNode
from htmlnode import LeafNode
from util import text_node_to_html_node

class TestTextNodeToHTMLNode(unittest.TestCase):

    
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("hello world", "text")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), 
            "hello world"
        )

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("hello world", "code")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), 
            "<code>hello world</code>"
        )

    def test_text_node_to_html_node_url(self):
        text_node = TextNode("hello world", "link", "https://www.google.com")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), 
            "<a href=\"https://www.google.com\">hello world</a>"
        )
    
    def test_text_node_to_html_node_image(self):
        text_node = TextNode("hello world", "image", "https://www.google.com")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), 
            "<img src=\"https://www.google.com\" alt=\"hello world\"></img>"
        )