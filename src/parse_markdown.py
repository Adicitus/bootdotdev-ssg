
import re
from textnode import TextNode, TextType

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
        
        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:len(node.text)], node.text_type, node.url))

    return new_nodes

def text_to_textnodes(text:str) -> list:
    node = TextNode(text, TextType.PLAIN)
    return split_nodes([node])

