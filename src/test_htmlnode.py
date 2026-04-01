import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="p", value="lorem ipsum", props={"id": "1"})
        node2 = HTMLNode(tag="p", value="lorem ipsum", props={"id": "1"})
        self.assertEqual(node, node2)

    def test_to_html1(self):
        node = HTMLNode(tag="p", value="lorem ipsum", props={"id": "1"})
        #self.assertEqual(node.to_html(), "p")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

class TestParentNode(unittest.TestCase):
    def test_parent_to_html_p(self):
        node = ParentNode("p", children=[LeafNode("b", "Hello, world!")])
        self.assertEqual(node.to_html(), "<p><b>Hello, world!</b></p>")

    def test_parent_to_html(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

