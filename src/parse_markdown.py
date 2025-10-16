
import re
from textnode import TextType, TextNode

def extract_markdown_images(text:str) -> list:
    images = []
    matches = re.finditer(r"(?P<image>!\[(?P<alt>[^\]]*)\]\((?P<url>[^\)]*)\))", text)

    for match in matches:
        images.append((match.group('alt'), match.group('url')))

    return images

def extract_markdown_links(text:str) -> list:
    links = []

    matches = re.finditer(r"(?P<link>\[(?P<anchor>[^\]]*)\]\((?P<url>[^\)]*)\))", text)
    for match in matches: links.append((match.group('anchor'), match.group('url')))


    return links

def split_nodes_delimiter(old_nodes, delimiter, text_type:TextType):
    new_nodes = []

    for node in old_nodes:
        parts = node.text.split(delimiter)
        
        n = len(parts)
        if n == 1:
            # node is already as granular as we can make it, keeping it.
            new_nodes.append(node)
            continue
        # We found the delimiters in the text, so we have more 
        # than 1 potential text nodes: every 2 part should correspond
        # to a node of text_type.
        for i in range(0, n):
            part = parts[i]
            if part == "": continue
            if i % 2 == 1:
                new_nodes.append(TextNode(part, text_type))
            else:
                new_nodes.append(TextNode(part, node.text_type))
    
    return new_nodes

        