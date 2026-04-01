import re
from enum import StrEnum
from dataclasses import dataclass

from src.convert import text_node_to_html_node
from src.htmlnode import HTMLNode, NodeProtocol, ParentNode, LeafNode
from src.textnode import text_to_textnodes

ol_regex = re.compile(r"^(?P<number>\d+)\.\s+", re.MULTILINE)
quote_regex = re.compile(r"^(> ?)", re.MULTILINE)
ul_regex = re.compile(r"^(- )", re.MULTILINE)
whitespace = re.compile(r"\s+")
code_block_parse = re.compile(r"^(?P<code>\w*)(\n)?", re.DOTALL)

class BlockType(StrEnum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def detect_ordered_list(block: str) -> bool:
    last_number = 0
    for line in block.splitlines():
        match = ol_regex.match(line.strip() + " ")
        if match is None:
            return False
        current_number = int(match.group("number"))
        if current_number - last_number != 1:
            return False
        last_number = current_number
    return True


def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(map(lambda s: s.startswith(">"), block.splitlines())):
        return BlockType.QUOTE
    if all(map(lambda s: s.startswith("- ") or s == "-", block.splitlines())):
        return BlockType.UNORDERED_LIST
    if detect_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


class BlockTag(StrEnum):
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    PRE = "pre"
    BLOCKQUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"
    LIST_ITEM = "li"
    PARAGRAPH = "p"
    DIV = "div"


def heading_block_to_html_node(block: str) -> ParentNode:
    symbol, block = block.split(" ", 1)
    children = list(map(text_node_to_html_node, text_to_textnodes(block)))
    match symbol:
        case "#":
            return ParentNode(BlockTag.H1, children=children)
        case "##":
            return ParentNode(BlockTag.H2, children=children)
        case "###":
            return ParentNode(BlockTag.H3, children=children)
        case "####":
            return ParentNode(BlockTag.H4, children=children)
        case "#####":
            return ParentNode(BlockTag.H5, children=children)
        case "######":
            return ParentNode(BlockTag.H6, children=children)
        case _:
            raise Exception(f"unknown block type: \n{block}")

def coding_block_to_html_node(block: str) -> ParentNode:
    block = block.strip("`")
    block = code_block_parse.sub("", block)

    return ParentNode(BlockTag.PRE, children=[LeafNode("code", value=block)])

def quote_block_to_html_node(block: str) -> ParentNode:
    block = quote_regex.sub("", block)
    children = list(map(text_node_to_html_node, text_to_textnodes(block)))
    return ParentNode(BlockTag.BLOCKQUOTE, children=children)

def unordered_list_block_to_html_node(block: str) -> ParentNode:
    block = ul_regex.sub("", block, re.MULTILINE)
    children = []
    for line in block.splitlines():
        nodes = list(map(text_node_to_html_node, text_to_textnodes(line)))
        children.append(ParentNode(BlockTag.LIST_ITEM, children=nodes))
    return ParentNode(BlockTag.UNORDERED_LIST, children=children)

def ordered_list_block_to_html_node(block: str) -> ParentNode:
    block = ol_regex.sub("", block)
    children = []
    for line in block.splitlines():
        nodes = list(map(text_node_to_html_node, text_to_textnodes(line)))
        children.append(ParentNode(BlockTag.LIST_ITEM, children=nodes))
    return ParentNode(BlockTag.ORDERED_LIST, children=children)

def block_to_html_node(block: str) -> NodeProtocol:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.HEADING:
            return heading_block_to_html_node(block)
        case BlockType.CODE:
            return coding_block_to_html_node(block)
        case BlockType.QUOTE:
            return quote_block_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_block_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_block_to_html_node(block)
        case BlockType.PARAGRAPH:
            children = list(map(text_node_to_html_node, text_to_textnodes(whitespace.sub(" ", block))))
            return ParentNode(BlockTag.PARAGRAPH, children=children)
        case _:
            raise Exception(f"unknown block type: \n{block}")
    # return ParentNode(BlockTag.DIV, children=[block_node])

