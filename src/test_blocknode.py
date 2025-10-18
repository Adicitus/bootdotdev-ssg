import unittest
from htmlnode import ParentNode, LeafNode
from blocknode import BlockNode, BlockType
from textnode import TextNode, TextType

class TestBlockNode(unittest.TestCase):
    def test_simple_paragraph_block(self):
        t = "This is a simple paragraph"
        node = BlockNode(BlockType.PARAGRAPH, t)
        self.assertIsInstance(node.textnodes, list)
        self.assertIsInstance(node.textnodes[0], TextNode)
        self.assertEqual(node.block_type, BlockType.PARAGRAPH)
        self.assertListEqual(
            [TextNode(t, TextType.PLAIN)],
            node.textnodes
        )
    
    def test_complex_paragraph_block(self):
        t = "**T**his is a _complex_ paragraph. See [nothing](nowhere) for details."
        node = BlockNode(BlockType.PARAGRAPH, t)
        self.assertIsInstance(node.textnodes, list)
        self.assertEqual(node.block_type, BlockType.PARAGRAPH)
        self.assertListEqual(
            [
                TextNode("T", TextType.BOLD),
                TextNode("his is a ", TextType.PLAIN),
                TextNode("complex", TextType.ITALIC),
                TextNode(" paragraph. See ", TextType.PLAIN),
                TextNode("nothing", TextType.LINK, "nowhere"),
                TextNode(" for details.", TextType.PLAIN),
            ],
            node.textnodes
        )
    
    def test_simple_quote_block(self):
        t = """
            > This is a quote.
            > It's not very quotable
        """
        node = BlockNode(BlockType.QUOTE, t)
        self.assertIsInstance(node.textnodes, list)
        self.assertEqual(node.block_type, BlockType.QUOTE)
        self.assertListEqual(
            [TextNode(t, TextType.PLAIN)],
            node.textnodes
        )
    
    def test_complex_quote_block(self):
        t = "This is a _quote_.\nIt's about a **boat**."
        node = BlockNode(BlockType.QUOTE, t)

        self.assertIsInstance(node.textnodes, list)
        self.assertEqual(node.block_type, BlockType.QUOTE)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.PLAIN),
                TextNode("quote", TextType.ITALIC),
                TextNode(".\nIt's about a ", TextType.PLAIN),
                TextNode("boat", TextType.BOLD),
                TextNode(".", TextType.PLAIN)
            ],
            node.textnodes
        )
    
    def test_block_to_html_node_simple_paragraph(self):
        t = "This is a simple paragraph"
        node = BlockNode(BlockType.PARAGRAPH, t)
        html_node = node.to_html_node()
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "p")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(
            LeafNode(None, t).__repr__(),
            html_node.children[0].__repr__()
        )
    
    def test_block_to_html_node_complex_paragraph(self):
        t = "**T**his is a _complex_ paragraph. See [nothing](nowhere) for details."
        node = BlockNode(BlockType.PARAGRAPH, t)
        html_node = node.to_html_node()
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "p")
        self.assertEqual(len(html_node.children), len(node.textnodes))
        self.assertListEqual(
            [
                TextNode("T", TextType.BOLD),
                TextNode("his is a ", TextType.PLAIN),
                TextNode("complex", TextType.ITALIC),
                TextNode(" paragraph. See ", TextType.PLAIN),
                TextNode("nothing", TextType.LINK, "nowhere"),
                TextNode(" for details.", TextType.PLAIN),
            ],
            node.textnodes
        )
        for i in range(0, len(html_node.children)):
            text_child, html_child = node.textnodes[i], html_node.children[i]
            match text_child.text_type:
                case TextType.PLAIN:
                    self.assertEqual(html_child.tag, None)
                    self.assertEqual(text_child.text, html_child.value)
                case TextType.BOLD:
                    self.assertEqual(html_child.tag, "b")
                    self.assertEqual(text_child.text, html_child.value)
                case TextType.ITALIC:
                    self.assertEqual(html_child.tag, "i")
                    self.assertEqual(text_child.text, html_child.value)
                case TextType.LINK:
                    self.assertEqual(html_child.tag, "a")
                    self.assertEqual(text_child.text, html_child.value)
                    self.assertEqual(text_child.url, html_child.props['href'])
    
    def test_markdown_blocks(self):
        t = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """
        
        node = BlockNode(BlockType.SECTION, t)
        node_html = node.to_html_node()
        html = node_html.to_html()
        self.assertEqual(
            html.replace("\n", " "),
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
