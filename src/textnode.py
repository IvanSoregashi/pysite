import re
from enum import StrEnum
from dataclasses import dataclass

image_regex = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
link_regex = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")


class TextType(StrEnum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


@dataclass(order=True)
class TextNode:
    text: str
    text_type: TextType
    url: str | None = None


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if delimiter in old_node.text:
            splits = old_node.text.split(delimiter)
            if len(splits) % 2 == 0:
                raise ValueError(f"Not even number of delimiters in the node {splits}")
            for i, split in enumerate(splits):
                new_node_type = text_type if i%2 else TextType.TEXT
                new_nodes.append(TextNode(text=split, text_type=new_node_type))
        else:
            new_nodes.append(old_node)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    images = image_regex.findall(text)
    return images

def extract_markdown_links(text: str) -> list[tuple]:
    images = link_regex.findall(text)
    return images


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text
        if "![" not in text:
            new_nodes.append(old_node)
            continue
        node_start = 0
        node_end = len(text)
        for result in image_regex.finditer(text):
            new_nodes.append(TextNode(text=text[node_start: result.start()], text_type=TextType.TEXT))
            link_text = text[result.regs[1][0]: result.regs[1][1]]
            link_href = text[result.regs[2][0]: result.regs[2][1]]
            new_nodes.append(TextNode(text=link_text, text_type=TextType.IMAGE, url=link_href))
            node_start = result.end()
        if node_start < node_end:
            new_nodes.append(TextNode(text=text[node_start: node_end], text_type=TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text
        if "[" not in text:
            new_nodes.append(old_node)
            continue
        node_start = 0
        node_end = len(text)
        for result in link_regex.finditer(text):
            new_nodes.append(TextNode(text=text[node_start: result.start()], text_type=TextType.TEXT))
            link_text = text[result.regs[1][0]: result.regs[1][1]]
            link_href = text[result.regs[2][0]: result.regs[2][1]]
            new_nodes.append(TextNode(text=link_text, text_type=TextType.LINK, url=link_href))
            node_start = result.end()
        if node_start < node_end:
            new_nodes.append(TextNode(text=text[node_start: node_end], text_type=TextType.TEXT))

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
