from textnode import TextNode
from textnode import TextType
from leafnode import LeafNode
from parentnode import ParentNode
from blocktype import (
    BlockType,
    block_to_block_type
)
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link
)


def main():
    text_object = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_object)


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", props={"href": text_node.url}, value=text_node.text)
        case TextType.IMAGE:
            return LeafNode(tag="img", props={"src": text_node.url, "alt": text_node.text}, value="")
        case _:
            raise Exception("Unfitting TextType")


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown):
    lines = [line if line.strip() else "" for line in markdown.split("\n")]
    cleaned_markdown = "\n".join(lines)
    blocks = cleaned_markdown.split("\n\n")
    blocks = [x.strip() for x in blocks if x.strip()]
    return blocks

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
                    if not line.startswith("> "):
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





if __name__ == "__main__":
    main()
