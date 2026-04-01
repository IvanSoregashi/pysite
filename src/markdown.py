from pathlib import Path

from src.blocknode import block_to_block_type, block_to_html_node, BlockType
from src.htmlnode import ParentNode


def markdown_to_blocks(markdown: str) -> list[str]:
    return [node.strip() for node in markdown.strip().split("\n\n")]


def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()
    return "No title"

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    # parent = ParentNode("html", children=[block_to_html_node(block) for block in blocks])
    parent = ParentNode("div", children=[block_to_html_node(block) for block in blocks])
    return parent

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = Path(from_path).read_text(encoding="utf-8")
    template = Path(template_path).read_text(encoding="utf-8")
    html_content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    dest = Path(dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"about to write to {dest}, {dest.exists()=}, {dest.is_dir()=}")
    dest.write_text(html, encoding="utf-8")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_dir = Path(dir_path_content)
    destination_dir = Path(dest_dir_path)
    for path in content_dir.rglob("*"):
        print(f"working on {path}")
        if path.is_dir():
            print(f"dirpath {path}")
            path.mkdir(parents=True, exist_ok=True)
            continue
        relative_path = path.relative_to(content_dir)
        dest_path = (destination_dir / relative_path).with_suffix(".html")
        print(f"generating {path} -> {dest_path}")
        generate_page(str(path), template_path, str(dest_path))