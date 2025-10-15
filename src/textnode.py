from enum import StrEnum

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
    
    def __eq__(self, other):
        return isinstance(other, TextNode) and self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        if self.url != None:
            return f"TextNode(\"{self.text}\", \"{self.text_type.value}\", \"{self.url}\")"
        else:
             return f"TextNode(\"{self.text}\", \"{self.txt_type}\")"
   

