import re

from src.textnode import TextNode, TextType

def extract_markdown_images(text:str) -> list:
    images = []
    matches = re.finditer(r"(?P<image>!\[(?P<alt>[^\]]*)\]\((?P<url>[^\)]*)\))", text)

    for match in matches:
        images.append((match.group('alt'), match.group('url')))

    return images
