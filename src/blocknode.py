import re
from enum import StrEnum
from parse_markdown import text_to_textnodes
from htmlnode import ParentNode, LeafNode

class BlockType(StrEnum):
    SECTION = "section"
    HEADING = "heading"
    CODE    = "code"
    QUOTE   = "quote"
    UNORDERED_LIST  = "unordered_list"
    ORDERED_LIST    = "ordered_list"
    PARAGRAPH       = "paragraph"

class BlockNode:
    def __init__(self, block_type:BlockType, text:str) -> None:
        self.raw_text = text
        self.block_type = block_type

        match block_type:
            case BlockType.SECTION:
                self.child_blocks = BlockNode.from_markdown(text)

            case BlockType.PARAGRAPH:
                self.textnodes = text_to_textnodes(text)

            case BlockType.HEADING:
                match = re.match(r"(?P<prefix>#{1,})[ ]+(?P<title>.*)", text)
                self.level = len(match.group('prefix'))
                self.textnodes = text_to_textnodes(match.group('title'))

            case BlockType.QUOTE:
                t = "\n".join(map(lambda s: s.strip('>'), text.split("\n")))
                self.textnodes = text_to_textnodes(t)

            case BlockType.CODE:
                # We'll be using the raw_text, so no pre-processing necessary
                pass

            case BlockType.UNORDERED_LIST:
                self.items = []

                for line in text.split("\n"):    
                    match = re.match(r"^- (?P<text>.*)$", line)
                    textnodes = text_to_textnodes(match.group('text'))
                    self.items.append((textnodes,))

            case BlockType.ORDERED_LIST:
                self.items = []

                for line in text.split("\n"):    
                    match = re.match(r"^(?P<number>\d+)\. (?P<text>.*)$", line)
                    textnodes = text_to_textnodes(match.group('text'))
                    self.items.append((textnodes, match.group('number')))
                
    def to_html_node(self):
        def textnodes_to_html(nodes) -> list:
            leafnodes = list(map(lambda n: n.to_html_node(), nodes))
            return leafnodes

        match self.block_type:
            case BlockType.SECTION:
                child_nodes = []
                for child in self.child_blocks:
                    child_node = child.to_html_node()
                    child_nodes.append(child_node)
                return ParentNode("div", child_nodes)
            case BlockType.PARAGRAPH:
                return ParentNode("p", textnodes_to_html(self.textnodes))
            case BlockType.HEADING:
                return ParentNode(f"h{self.level}", textnodes_to_html(self.textnodes))
            case BlockType.QUOTE:
                return ParentNode("blockquote", textnodes_to_html(self.textnodes))
            case BlockType.CODE:
                return LeafNode("code", self.raw_text)

            case BlockType.UNORDERED_LIST:
                childnodes = []
                for item in self.items:
                    childnodes.append(ParentNode("li", textnodes_to_html(self.textnodes)))
                return ParentNode("ul", childnodes)

            case BlockType.ORDERED_LIST:
                childnodes = []
                for item in self.items:
                    childnodes.append(ParentNode("li", textnodes_to_html(self.textnodes)))
                return ParentNode("ol", childnodes)
    
    def __eq__(self, other):
        if not isinstance(other, BlockNode): return False
        return self.block_type == other.block_type and self.raw_text == other.raw_text
    
    def __repr__(self):
        return f"BlockNode({self.block_type}, {self.raw_text})"

        


    @staticmethod
    def from_markdown(markdown_text):
        blocks = []
        
        state = {
            "block": [],
            "blocktype": None
        }

        def store_block():
            if len(state["block"]) > 0:
                glue = "\n"
                blocks.append(BlockNode(state["blocktype"], glue.join(state["block"])))
                state["block"] = []
                state["blocktype"] = None

        for line in markdown_text.split("\n"):
            if state["blocktype"] != BlockType.CODE: line = line.strip()

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


    



