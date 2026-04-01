import unittest

from textnode import TextNode, TextType
from convert import text_node_to_html_node

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("Lorem Ipsum", TextType.TEXT)
        self.assertEqual(text_node_to_html_node(node).to_html(), "Lorem Ipsum")

    def test_bold(self):
        node = TextNode("Lorem Ipsum", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<b>Lorem Ipsum</b>")

    def test_italic(self):
        node = TextNode("Lorem Ipsum", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<i>Lorem Ipsum</i>")

    def test_code(self):
        node = TextNode("print('Lorem Ipsum')", TextType.CODE)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<code>print('Lorem Ipsum')</code>")

    def test_link(self):
        node = TextNode("Lorem Ipsum", TextType.LINK, "https://www.google.com")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<a href="https://www.google.com">Lorem Ipsum</a>')

    def test_image(self):
        node = TextNode("Lorem Ipsum", TextType.IMAGE, "https://www.google.com/tre/1.jpg")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<img src="https://www.google.com/tre/1.jpg" alt="Lorem Ipsum"></img>')

