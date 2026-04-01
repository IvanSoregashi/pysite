import unittest

from src.markdown import markdown_to_blocks
from src.textnode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, \
    split_nodes_image, text_to_textnodes
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_ne_with_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot2.dev")

    def test_splitting_text(self):
        print()
        node = TextNode("This is a **text** node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", text_type=TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(str(new_nodes), str([
        TextNode(text="This is a ", text_type=TextType.TEXT),
        TextNode(text="text", text_type=TextType.BOLD),
        TextNode(text=" node", text_type=TextType.TEXT),
        ]))

    def test_splitting_text2(self):
        print()
        node = TextNode("This is a **text** node __ italic text__is also here __twice__", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", text_type=TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "__", text_type=TextType.ITALIC)
        self.assertEqual(str(sorted(new_nodes)), str(sorted([
            TextNode(text="This is a ", text_type=TextType.TEXT),
            TextNode(text="text", text_type=TextType.BOLD),
            TextNode(text=" node ", text_type=TextType.TEXT),
            TextNode(text=" italic text", text_type=TextType.ITALIC),
            TextNode(text="is also here ", text_type=TextType.TEXT),
            TextNode(text="twice", text_type=TextType.ITALIC),
            TextNode(text="", text_type=TextType.TEXT),
        ])))

    def test_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])

    def test_link_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_link_splitting(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        for n1, n2 in zip(new_nodes,
                              [
                                  TextNode("This is text with a link ", TextType.TEXT),
                                  TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                                  TextNode(" and ", TextType.TEXT),
                                  TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                              ]
                          ):
            self.assertEqual(str(n1), str(n2))

    def test_image_splitting(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev/1.png) and ![to youtube](https://www.youtube.com/@bootdotdev/1.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        for n1, n2 in zip(new_nodes,
                              [
                                  TextNode("This is text with a link ", TextType.TEXT),
                                  TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev/1.png"),
                                  TextNode(" and ", TextType.TEXT),
                                  TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev/1.png"),
                              ]
                          ):
            self.assertEqual(str(n1), str(n2))

    def test_splitting(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        for n1, n2 in zip(text_to_textnodes(text), [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
    ]):
            self.assertEqual(str(n1), str(n2))


    def test_md_splitting(self):
        md = \
"""
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# This is a heading", "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.", "- This is the first list item in a list block\n- This is a list item\n- This is another list item"])

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()
