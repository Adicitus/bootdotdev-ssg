
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

def split_nodes_image(old_nodes:list) -> list:
    new_nodes = []

    for node in old_nodes:
        matches = re.finditer(r"!\[(?P<alt>[^\]]*)\]\((?P<url>[^\)]*)\)", node.text)
        last_index = 0
        for match in matches:
            start_index = match.start()
            end_index = match.end()

            if last_index < start_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], node.text_type, node.url))
            
            new_nodes.append(TextNode(match.group('alt'), TextType.IMAGE, match.group('url')))
            last_index = end_index

    return new_nodes

def split_nodes_link(old_nodes:list) -> list:
    new_nodes = []

    for node in old_nodes:
        matches = re.finditer(r"\[(?P<anchor>[^\]]*)\]\((?P<url>[^\)]*)\)", node.text)
        last_index = 0
        for match in matches:
            start_index = match.start()
            end_index = match.end()

            if last_index < start_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], node.text_type, node.url))
            
            new_nodes.append(TextNode(match.group('anchor'), TextType.LINK, match.group('url')))
            last_index = end_index

    return new_nodes

patterns = {
    TextType.BOLD:      r"(?P<el_bold>\*\*(?P<bold_text>[^*]+)\*\*)",
    TextType.ITALIC:    r"(?P<el_italic>_(?P<italic_text>[^_]+)_)",
    TextType.CODE:      r"(?P<el_code>`(?P<code_text>[^`]+)`)",
    TextType.LINK:      r"(?P<el_link>\[(?P<anchor>[^\]]*)\]\((?P<link_url>[^\)]*)\))",
    TextType.IMAGE:     r"(?P<el_image>!\[(?P<alt>[^\]]*)\]\((?P<image_url>[^\)]*)\))"
}

patterns['all'] = f"({"|".join(patterns.values())})"

def split_nodes(old_nodes:list) -> list:
    new_nodes = []
    for node in old_nodes:
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

    return new_nodes

def text_to_textnodes(text:str) -> list:
    node = TextNode(text, TextType.PLAIN)
    return split_nodes([node])