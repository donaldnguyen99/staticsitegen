import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "google.com")
        self.assertEqual(f"{node}", "TextNode(This is a text node, bold, google.com)")

    def test_url_none(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.url, None)

    def test_text_type_neq(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is also a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", "boot.dev")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
