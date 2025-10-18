from enum import StrEnum
from htmlnode import LeafNode

class TextType(StrEnum):
    PLAIN   = "plain"
    BOLD    = "bold"
    ITALIC  = "italic"
    CODE    = "code"
    LINK    = "link"
    IMAGE   = "image"

class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type if isinstance(text_type, TextType) else TextType(text_type)
        self.url = url
    
    def to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.PLAIN:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise ValueError(f"unsupported text type: {self.type}")

    def __eq__(self, other) -> bool:
        return isinstance(other, TextNode) and self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self) -> str:
        if self.url != None:
            return f"TextNode(\"{self.text}\", \"{self.text_type.value}\", \"{self.url}\")"
        else:
             return f"TextNode(\"{self.text}\", \"{self.text_type.value}\")"
   

