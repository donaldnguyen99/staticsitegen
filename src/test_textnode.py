import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertEqual(f"{node}", "TextNode(This is a text node, bold, google.com)")

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_text_type_neq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "boot.dev")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
