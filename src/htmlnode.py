from dataclasses import dataclass
from typing import Protocol


class NodeProtocol(Protocol):
    def to_html(self) -> str: ...


@dataclass(kw_only=True)
class PropsMixin:
    props: dict | None = None

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())


@dataclass(kw_only=True)
class ParentMixin:
    children: list[NodeProtocol]

    def render_children(self) -> str:
        if not self.children:
            return ""
        children = [child.to_html() for child in self.children]
        children_text = "".join(children)
        return children_text


@dataclass
class HTMLNode(PropsMixin, ParentMixin):
    tag: str | None = None
    value: str | None = None
    children: list[NodeProtocol] | None = None

    def to_html(self):
        raise NotImplementedError()


@dataclass
class LeafNode(PropsMixin):
    tag: str | None
    value: str

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("ParentNode must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


@dataclass
class ParentNode(PropsMixin, ParentMixin):
    tag: str

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have at least one child node")
        return f"<{self.tag}{self.props_to_html()}>{self.render_children()}</{self.tag}>"
