
import re
from textnode import TextNode, TextType

def split_nodes(old_nodes:list) -> list:
    new_nodes = []
    for node in old_nodes:
        node.split(new_nodes)

    return new_nodes

def text_to_textnodes(text:str) -> list:
    node = TextNode(text, TextType.PLAIN)
    return split_nodes([node])

