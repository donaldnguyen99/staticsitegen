import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self):
        node = HTMLNode("p", "Text here")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Text here")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_to_html(self):
        node = HTMLNode("p", "Text here")
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode("a", "link", None, 
            {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), 
            " href=\"https://www.google.com\" target=\"_blank\"")