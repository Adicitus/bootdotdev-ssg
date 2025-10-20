import re
from enum import StrEnum
from htmlnode import LeafNode

class TextType(StrEnum):
    PLAIN   = "plain"
    BOLD    = "bold"
    ITALIC  = "italic"
    CODE    = "code"
    LINK    = "link"
    IMAGE   = "image"

patterns = {
    TextType.BOLD:      r"(?P<el_bold>\*\*(?P<bold_text>[^*]+)\*\*)",
    TextType.ITALIC:    r"(?P<el_italic>_(?P<italic_text>[^_]+)_)",
    TextType.CODE:      r"(?P<el_code>`(?P<code_text>[^`]+)`)",
    TextType.LINK:      r"(?P<el_link>\[(?P<anchor>[^\]]*)\]\((?P<link_url>[^\)]*)\))",
    TextType.IMAGE:     r"(?P<el_image>!\[(?P<alt>[^\]]*)\]\((?P<image_url>[^\)]*)\))"
}

patterns['all'] = f"({"|".join(patterns.values())})"

class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type if isinstance(text_type, TextType) else TextType(text_type)
        self.url = url
    
    def split(self, new_nodes=[]) -> list:
        node = self

        matches = re.finditer(patterns['all'], node.text)
        last_index = 0
        for match in matches:
            start_index = match.start()
            end_index = match.end()
            if last_index < start_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], node.text_type, node.url))
            
            values = match.groupdict()
            node_type = list(filter(lambda k: k.startswith("el_") and values[k] != None, values.keys()))[0].split('_')[1]

            match node_type:
                case "bold":
                    new_nodes.append(TextNode(values['bold_text'], TextType.BOLD))
                case "italic":
                    new_nodes.append(TextNode(values['italic_text'], TextType.ITALIC))
                case "code":
                    new_nodes.append(TextNode(values['code_text'], TextType.CODE))
                case "link":
                    new_nodes.append(TextNode(values['anchor'], TextType.LINK, values['link_url']))
                case "image":
                    new_nodes.append(TextNode(values['alt'], TextType.IMAGE, values['image_url']))
            
            last_index = end_index
        
        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:len(node.text)], node.text_type, node.url))

        return new_nodes
    
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
   

