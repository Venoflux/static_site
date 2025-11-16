import unittest
from blocktype import (
    BlockType,
    block_to_block_type,
    extract_title
)

class TestBlockType(unittest.TestCase):
    def test_paragraph(self):
        markdown_block = "This is a paragraph."
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_header(self):
        markdown_block = "## Header"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.HEADING)

    # TODO: Write more test for each BlockType case
    def test_code(self):
        markdown_block = "```\nprint('Hello World!')\n```"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote(self):
        markdown_block = ">This is a quote\n>This is a quote too!"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_unordered_list(self):
        markdown_block = "- This is an unordered list\n- This is another member"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        markdown_block = "1. First\n2. Second\n3. Third"
        block_type = block_to_block_type(markdown_block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_empty_string(self):
        block_type = block_to_block_type("")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_extract_title(self):
        title = extract_title("# Hello ")
        self.assertEqual(title, "Hello")
