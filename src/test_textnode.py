import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)


    def test_url_eq(self):
        node = TextNode("google", TextType.LINK, "https://www.google.com/")
        node2 = TextNode("google", TextType.LINK, "https://www.google.com/")
        self.assertEqual(node, node2)

    
if __name__ == "__main__":
    unittest.main()
