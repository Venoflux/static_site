import os
import shutil
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
import copy_static


def main():
    abs_path = os.path.abspath(os.getcwd())
    listdir = os.listdir(os.path.abspath(os.getcwd()))

    if "public" in listdir:
        print("Deleting public directory...")
        shutil.rmtree("./public")

    if "static" not in listdir:
        raise Exception("static file not found")
    
    print("Creating public directory...")
    public_path = os.path.join(abs_path, "public")
    os.mkdir(public_path)

    copy_static.static_to_public("")


def extract_title(markdown):
    pass



if __name__ == "__main__":
    main()
