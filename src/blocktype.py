from enum import Enum

from parentnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import (
    text_node_to_html_node,
    TextNode,
    TextType
)


class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5


def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return "Title"

    
def markdown_to_blocks(markdown):
    lines = [line if line.strip() else "" for line in markdown.split("\n")]
    cleaned_markdown = "\n".join(lines)
    blocks = cleaned_markdown.split("\n\n")
    blocks = [x.strip() for x in blocks if x.strip()]
    return blocks


def block_to_block_type(markdown_block):
    if not markdown_block:
        return BlockType.PARAGRAPH
    
    # Check if markdown block is a header/heading
    if markdown_block[0] == "#":
        header_slice = markdown_block.split(" ")[0]
        if header_slice[0] == "#" and len(header_slice) <= 6:
            is_sharp = True
            for char in header_slice:
                if char != "#":
                    is_sharp = False
                    break
            if is_sharp:
                return BlockType.HEADING

    # Check if markdown block is a code block
    is_code = True
    for i in range(3):
        if markdown_block[i] != "`" or markdown_block[(len(markdown_block) - 1) - i] != "`":
            is_code = False
            break
    if is_code:
        return BlockType.CODE

    # Check if markdown block is a quote block
    if markdown_block[0] == ">":
        quote_split = markdown_block.split("\n")
        is_quote = True
        for line in quote_split:
            if line[0] != ">":
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE

    # Check if markdown block is an unordered list
    if markdown_block[:2] == "- ":
        is_unordered_list = True
        unordered_split = markdown_block.split("\n")
        for line in unordered_split:
            if line[:2] != "- ":
                is_unordered_list = False
                break
        if is_unordered_list:
            return BlockType.UNORDERED_LIST

    # Check if markdown block is an ordered list
    if markdown_block[0].isdigit() and markdown_block[1:3] == ". ":
        is_ordered_list = True
        ordered_split = markdown_block.split("\n")
        for line in ordered_split:
            if not line[0].isdigit() or line[1:3] != ". ":
                is_ordered_list = False
                break
        if is_ordered_list:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                if not block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
                    raise ValueError("invalid header block")
                split_header = block.split(" ")
                header_level = len(split_header[0])
                header_text = " ".join(split_header[1:])
                children = text_to_children(header_text)
                html_nodes.append(ParentNode(tag=f"h{header_level}", children=children))
                
            case BlockType.CODE:
                if not block.startswith("```") or not block.endswith("```"):
                    raise ValueError("invalid code block")
                text = block[4:-3]
                raw_text_node = TextNode(text, TextType.TEXT)
                child = text_node_to_html_node(raw_text_node)
                code = ParentNode("code", [child])
                html_nodes.append(ParentNode("pre", [code]))
                
            case BlockType.QUOTE:
                clean_markdown = ""
                lines = block.split('\n')
                for line in lines:
                    if not line.startswith(">"):
                        raise ValueError("invalid quote block")
                    clean_markdown += line[2:] + " "
                clean_markdown = clean_markdown.strip()
                children = text_to_children(clean_markdown)
                html_nodes.append(ParentNode("blockquote", children))
                
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                html_items = []
                for line in lines:
                    if not line.startswith("- "):
                        raise ValueError("invalid unordered list block")
                    text = line[2:]
                    children = text_to_children(text)
                    html_items.append(ParentNode("li", children))
                html_nodes.append(ParentNode("ul", html_items))
                
            case BlockType.ORDERED_LIST:
                items = block.split("\n")
                html_items = []
                for item in items:
                    text = item[3:]
                    children = text_to_children(text)
                    html_items.append(ParentNode("li", children))
                html_nodes.append(ParentNode("ol", html_items))
                
            case _:
                lines = block.split("\n")
                paragraph = " ".join(lines)
                paragraph = " ".join(paragraph.split())
                children = text_to_children(paragraph)
                html_nodes.append(ParentNode(tag="p", children=children))                
    return ParentNode(tag="div", children=html_nodes)
