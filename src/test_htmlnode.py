import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self):
        node = HTMLNode("p", "Text here")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Text here")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_to_html_error(self):
        node = HTMLNode("p", "Text here")
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode("a", "link", None, 
            {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), 
            " href=\"https://www.google.com\" target=\"_blank\"")
        
    def test_props_to_html_none(self):
        node = HTMLNode("a", "link", None, None)
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_leafnode(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph of text.")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def create_leafnode_no_value(self):
        return LeafNode("p", None, {"href": "https://google.com"})

    def test_leafnode_value_error(self):
        self.assertRaises(ValueError, self.create_leafnode_no_value)
    
    def test_leafnode_children_none(self):
        node = LeafNode("a", "This is a link", {"href": "google.com"})
        self.assertEqual(node.children, None)

    def test_leafnode_to_html(self):
        node = LeafNode("a", "link",
            {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            node.to_html(), 
            "<a href=\"https://www.google.com\" target=\"_blank\">link</a>")
        
class TestParentNode(unittest.TestCase):
    def test_parentnode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, None)
        self.assertNotEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_parentnode_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(isinstance(node.children, list), True)
        self.assertEqual(len(node.children), 4)
        self.assertEqual(isinstance(node.children[0], HTMLNode), True)

    def test_parentnode_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parentnode_to_html_nested1(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "Item 1"),
                        LeafNode("li", "Item 2"),
                        ParentNode("li", 
                            [
                                LeafNode("b", "Bold Item 3")
                            ]
                        )
                    ]
                ),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><ul><li>Item 1</li><li>Item 2</li><li><b>Bold Item 3</b></li></ul>Normal text<i>italic text</i>Normal text</p>")

    def test_parentnode_to_html_nested2(self):
        node = ParentNode(
            "body",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("i", "Italicized text")
                    ]
                )
            ]
        )
        self.assertEqual(node.to_html(), "<body><p><i>Italicized text</i></p></body>")