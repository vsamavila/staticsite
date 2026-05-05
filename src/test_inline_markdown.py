import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_no_delimiter(self):
        node = TextNode("plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "plain text")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_split_simple_bold_middle(self):
        node = TextNode("this is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_bold_at_start(self):
        node = TextNode("**bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_bold_at_end(self):
        node = TextNode("text **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("text ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_split_multiple_bold(self):
        node = TextNode("**one** and **two**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
            ],
        )

    def test_split_code_after_bold_pass(self):
        nodes = [
            TextNode("hey ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" `CODE` here", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("hey ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("CODE", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_unbalanced_raises(self):
        node = TextNode("this is **broken text", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_text_to_textnodes_bold_only(self):
        nodes = text_to_textnodes("Hello **world** today")
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0], TextNode("Hello ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("world", TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(" today", TextType.TEXT))

    def test_markdown_to_blocks(self):
        md = """
This is one block

This is another block
that continues on a second line

- list item 1
- list item 2
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is one block",
                "This is another block\nthat continues on a second line",
                "- list item 1\n- list item 2"
            ],
        )






if __name__ == "__main__":
    unittest.main()
