import re

from src.textnode import TextNode, TextType

def extract_markdown_links(text:str) -> list:
    links = []

    matches = re.finditer(r"(?P<link>\[(?P<anchor>[^\]]*)\]\((?P<url>[^\)]*)\))", text)
    for match in matches: links.append((match.group('anchor'), match.group('url')))


    return links