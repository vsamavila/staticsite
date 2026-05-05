import unittest

from markdown_blocks import markdown_to_html_node, block_to_block_type, BlockType
from inline_markdown import markdown_to_blocks

class TestMarkdownBlocks(unittest.TestCase):

    def test_paragraph(self):
        block = "this is a normal paragraph"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_heading_h1(self):
        block = "# heading"
        assert block_to_block_type(block) == BlockType.HEADING

    def test_heading_h6(self):
        block = "###### heading"
        assert block_to_block_type(block) == BlockType.HEADING

    def test_heading_requires_space(self):
        block = "#heading"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_heading_rejects_h7(self):
        block = "####### heading"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_heading_rejects_multiline_block(self):
        block = "# heading\nextra line"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_code_block(self):
        block = "```\nthis is code\n```"
        assert block_to_block_type(block) == BlockType.CODE

    def test_code_block_multiline(self):
        block = "```\nline one\nline two\n```"
        assert block_to_block_type(block) == BlockType.CODE

    def test_code_block_requires_newline_after_opening_backticks(self):
        block = "```code\n```"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_code_block_requires_closing_backticks_on_own_line(self):
        block = "```\ncode here ```"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_quote_block_without_space(self):
        block = ">hello\n>world"
        assert block_to_block_type(block) == BlockType.QUOTE

    def test_quote_block_with_space(self):
        block = "> hello\n> world"
        assert block_to_block_type(block) == BlockType.QUOTE

    def test_quote_block_rejects_line_without_greater_than(self):
        block = "> hello\nworld"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_unordered_list(self):
        block = "- item one\n- item two\n- item three"
        assert block_to_block_type(block) == BlockType.ULIST

    def test_unordered_list_requires_space(self):
        block = "-item one\n- item two"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_unordered_list_rejects_malformed_line(self):
        block = "- item one\nitem two"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_ordered_list(self):
        block = "1. item one\n2. item two\n3. item three"
        assert block_to_block_type(block) == BlockType.OLIST

    def test_ordered_list_must_start_at_one(self):
        block = "2. item one\n3. item two"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_ordered_list_must_increment_by_one(self):
        block = "1. item one\n3. item three"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_ordered_list_requires_space_after_dot(self):
        block = "1.item one\n2. item two"
        assert block_to_block_type(block) == BlockType.PARAGRAPH

    def test_ordered_list_rejects_malformed_line(self):
        block = "1. item one\nhello"
        assert block_to_block_type(block) == BlockType.PARAGRAPH


    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()

    
