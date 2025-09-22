from enum import Enum


class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, text_node):
        text_equal = self.text == text_node.text
        type_equal = self.text_type == text_node.text_type
        url_equal = self.url == text_node.url

        return text_equal and type_equal and url_equal

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
