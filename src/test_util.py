import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from util import (text_node_to_html_node, split_nodes_delimiter,\
                 extract_markdown_images, extract_markdown_links,\
                 split_nodes_image, split_nodes_link, split_nodes_link_helper,\
                 text_to_textnodes, markdown_to_blocks, block_to_block_type)

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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )
    
    def test_extract_markdown_images_no_alt(self):
        text = "This is text with a ![](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            extract_markdown_images(text),
            [("", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_extract_markdown_images_no_alt_url(self):
        text = "This is text with a ![]() and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            extract_markdown_images(text),
            [("", ""), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            extract_markdown_links(text),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )
    
    def test_extract_markdown_links_no_alt(self):
        text = "This is text with a link [](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            extract_markdown_links(text),
            [("", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    def test_extract_markdown_links_no_alt_url(self):
        text = "This is text with a link []() and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            extract_markdown_links(text),
            [("", ""), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
                ),
            ]
        )

    def test_split_nodes_image_only_one(self):
        node = TextNode("![first_image](https://myurl.png)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("first_image", TextType.IMAGE, "https://myurl.png")
            ]
        )
    
    def test_split_nodes_image_only_two(self):
        node = TextNode("![first_image](https://myurl.png)![second](my.url.jpeg)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("first_image", TextType.IMAGE, "https://myurl.png"),
                TextNode("second", TextType.IMAGE, "my.url.jpeg")
            ]
        )

    def test_split_nodes_image_only_two_with_text(self):
        node = TextNode("Hi!![first_image](https://myurl.png) ![second](my.url.jpeg)world!", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("Hi!", TextType.TEXT),
                TextNode("first_image", TextType.IMAGE, "https://myurl.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "my.url.jpeg"),
                TextNode("world!", TextType.TEXT),
            ]
        )
    
    def test_split_nodes_image_only_two_with_no_starting_text(self):
        node = TextNode("![first_image](https://myurl.png) ![second](my.url.jpeg)world!", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("first_image", TextType.IMAGE, "https://myurl.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "my.url.jpeg"),
                TextNode("world!", TextType.TEXT),
            ]
        )

    def test_split_nodes_image_only_part_of_image(self):
        node = TextNode("![first_image]", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("![first_image]", TextType.TEXT)
            ]
        )

    def test_split_nodes_image_only_text_no_url(self):
        node = TextNode("some text ![asdf]()", TextType.TEXT)
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("some text ", TextType.TEXT),
                TextNode("asdf", TextType.IMAGE, "")
            ]
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ]
        )

    def test_split_nodes_link_only_one(self):
        node = TextNode("[first_link](https://myurl.png)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("first_link", TextType.LINK, "https://myurl.png")
            ]
        )
    
    def test_split_nodes_link_only_two(self):
        node = TextNode("[first_link](https://myurl.png)[second](my.url.jpeg)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("first_link", TextType.LINK, "https://myurl.png"),
                TextNode("second", TextType.LINK, "my.url.jpeg")
            ]
        )

    def test_split_nodes_link_only_two_with_text(self):
        node = TextNode("Hi!![first_link](https://myurl.png) [second](my.url.jpeg)world!", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("Hi!!", TextType.TEXT),
                TextNode("first_link", TextType.LINK, "https://myurl.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("second", TextType.LINK, "my.url.jpeg"),
                TextNode("world!", TextType.TEXT),
            ]
        )
    
    def test_split_nodes_link_only_two_with_no_starting_text(self):
        node = TextNode("[first_link](https://myurl.png) [second](my.url.jpeg)world!", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("first_link", TextType.LINK, "https://myurl.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("second", TextType.LINK, "my.url.jpeg"),
                TextNode("world!", TextType.TEXT),
            ]
        )

    def test_split_nodes_link_only_part_of_link(self):
        node = TextNode("[first_link]", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("[first_link]", TextType.TEXT)
            ]
        )

    def test_split_nodes_link_only_text_no_url(self):
        node = TextNode("some text ![asdf]()", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("some text !", TextType.TEXT),
                TextNode("asdf", TextType.LINK, "")
            ]
        )


class TestSplitNodesLinkHelper(unittest.TestCase):
    def test_split_nodes_link_helper_default(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_link_helper([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ]
        )

    def test_split_nodes_link_helper_image(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_link_helper([node], TextType.IMAGE),
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
                ),
            ]
        )
    
    def test_split_nodes_link_helper_wrong_text_type(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        with self.assertRaises(ValueError):
            split_nodes_link_helper([node], TextType.BOLD)


class TestTextToTextNode(unittest.TestCase):
    def test_text_to_text_node_all(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )
    
    def test_text_to_text_node_no_split(self):
        text = "This is "
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT)
            ]
        )

    def test_text_to_text_node_only_delimiters(self):
        text = "This is **text** with an *italic* word and a `code block`"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE)
            ]
        )

    def test_text_to_text_node_only_image_link(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )
    

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        self.assertListEqual(
            markdown_to_blocks(markdown),
            [
                "# This is a heading",

                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",

"""* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ]
        )
    
    def test_markdown_to_blocks_multiple_newlines(self):
        markdown = """# This is a heading

        
This is a paragraph of text. It has some **bold** and *italic* words inside of it.





* This is the first list item in a list block
* This is a list item
* This is another list item"""
        self.assertListEqual(
            markdown_to_blocks(markdown),
            [
                "# This is a heading",

                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",

"""* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ]
        )

    def test_markdown_to_blocks_one_block(self):
        markdown = """# This is a heading"""
        self.assertListEqual(
            markdown_to_blocks(markdown),
            [
                "# This is a heading"
            ]
        )

    def test_markdown_to_blocks_one_block_footer_header(self):
        markdown = """\n\n# This is a heading
        
        """
        self.assertListEqual(
            markdown_to_blocks(markdown),
            [
                "# This is a heading"
            ]
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "asdf\nasdf\nasdf"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_to_block_type_ordered_list(self):
        block = "1. asdf\n2. asdf\n3. asdf"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_block_to_block_type_unordered_list_asterisk(self):
        block = "* asdf\n* asdf\n* asdf"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_block_to_block_type_unordered_list_hyphen(self):
        block = "- asdf\n- asdf\n- asdf"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_block_to_block_type_quote(self):
        block = ">asdf\n> asdf\n>asdf"
        self.assertEqual(block_to_block_type(block), "quote")
    
    def test_block_to_block_type_code(self):
        block = "```>asdf\n> asdf\n>asdf```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_block_to_block_type_heading(self):
        block = "### Heading"
        self.assertEqual(block_to_block_type(block), "heading")

if __name__ == "__main__":
    unittest.main()