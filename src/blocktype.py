from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5


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
