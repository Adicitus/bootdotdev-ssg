
import re
from enum import StrEnum
from textnode import TextType, TextNode

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


class BlockType(StrEnum):
    HEADING = "heading"
    CODE    = "code"
    QUOTE   = "quote"
    UNORDERED_LIST  = "unordered_list"
    ORDERED_LIST    = "ordered_list"
    PARAGRAPH       = "paragraph"


def markdown_to_blocks(markdown_text):
    blocks = []
    
    state = {
        "block": [],
        "blocktype": None
    }

    def store_block():
        if len(state["block"]) > 0:
            blocks.append((state["blocktype"], "\n".join(state["block"])))
            state["block"] = []
            state["blocktype"] = None

    for line in markdown_text.split("\n"):
        line = line.strip()

        if re.match(r"^\s*$", line):
            # This line is blank, implying that the previous block has ended.
            store_block()
            continue
        
        if re.match(r"^#{1,6} ", line):
            # This line is a heading, which is it's own block, implying that the previous block has ended.
            # This is a single line block.
            store_block()
            state["block"].append(line)
            state["blocktype"] = BlockType.HEADING
            store_block()
            continue
        
        if re.match(r"^```", line):
            # This is the first or last line of a code block, either way we should store any block we are currently building.
            if state["blocktype"] != None: store_block()
            state["blocktype"] = BlockType.CODE
            continue
            
        if re.match(r"^>", line):
            # This is a quote block, every line has to start with the '>'.
            if state["blocktype"] != BlockType.QUOTE:
                store_block()
                state["blocktype"] = BlockType.QUOTE
        
        if re.match(r"^-", line):
            # This is a unordered list item, every line in the list must start with '-'
            if state["blocktype"] != BlockType.UNORDERED_LIST:
                store_block()
                state["blocktype"] = BlockType.UNORDERED_LIST

        if re.match(r"^\d+\.", line):
            # This is a unordered list item, every line in the list must start with a number and a period.
            if state["blocktype"] != BlockType.ORDERED_LIST:
                store_block()
                state["blocktype"] = BlockType.ORDERED_LIST
        
        # At this point this is a non-empty line, if we have not identified the block type, it's a paragraph.
        if state["blocktype"] == None: state["blocktype"] = BlockType.PARAGRAPH
        
        # Add the line to our current block.
        state["block"].append(line)
    
    # If the document doesn't end with a new line, we need to store the block we're currently building before returning the blocks.
    if len(state["block"]) > 0:
        blocks.append("\n".join(state["block"]))
    
    return blocks

