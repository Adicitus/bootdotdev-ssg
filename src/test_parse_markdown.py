import unittest
from textnode import TextNode, TextType
from blocknode import BlockNode, BlockType
from parse_markdown import split_nodes, text_to_textnodes

class TestSplitNodes(unittest.TestCase):
    
    def test_split_nodes(self):
        node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.PLAIN)
        new_nodes = split_nodes([node])

        self.assertIsInstance(new_nodes, list)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_text_to_textnodes_simple_paragraph(self):
        t = "This is a simple paragraph"
        nodes = text_to_textnodes(t)
        self.assertIsInstance(nodes, list)
        self.assertListEqual(
            [TextNode(t, TextType.PLAIN)],
            nodes
        )

    def test_text_to_textnodes_mixed_elements(self):
        t = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(t)

        self.assertIsInstance(nodes, list)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )
    
    def test_markdown_to_blocks(self):
        t = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

            - This is the first list item in a list block
            - This is a list item
            - This is another list item
        """

        blocks = BlockNode.from_markdown(t)
        self.assertListEqual(
            [
                BlockNode(BlockType.HEADING, "# This is a heading"),
                BlockNode(BlockType.PARAGRAPH, "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."),
                BlockNode(BlockType.UNORDERED_LIST, "- This is the first list item in a list block\n- This is a list item\n- This is another list item")
            ],
            blocks
        )