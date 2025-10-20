import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode

class TestTextType(unittest.TestCase):
    def test_equivalence(self):
        self.assertEqual(TextType.BOLD, "bold")

    def test_invalid_type(self):
        with self.assertRaises(Exception):
            TextNode("Test", "invalid_type")

class TestTextNode(unittest.TestCase):
    def test_url_default_none(self):
        node1 =  TextNode("This is a text node", TextType.PLAIN)
        self.assertEqual(node1.url, None)

    def test_eq_identity(self):
        node1 =  TextNode("This is a text node", TextType.BOLD)
        node2 =  TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
    
    def test_eq_different_types(self):
        node1 =  TextNode("This is a text node", TextType.BOLD)
        node2 =  TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
    
    def test_eq_different_text(self):
        node1 =  TextNode("This is a text node", TextType.BOLD)
        node2 =  TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)
    
    def test_eq_different_url(self):
        node1 =  TextNode("This is a text node", TextType.BOLD, "http://localhost")
        node2 =  TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)
    
    def test_split_nodes(self):
        node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.PLAIN)
        new_nodes = node.split()

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

class TestTextToHTML(unittest.TestCase):
    def test_plaintext(self):
        text_node = TextNode("a", TextType.PLAIN)
        html_node = text_node.to_html_node()
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.to_html(), text_node.text)
    
    def test_bold(self):
        text_node = TextNode("a", TextType.BOLD)
        html_node = text_node.to_html_node()
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), f"<b>a</b>")
    
    def test_italic(self):
        text_node = TextNode("a", TextType.ITALIC)
        html_node = text_node.to_html_node()
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), f"<i>a</i>")
    
    def test_code(self):
        text_node = TextNode("a", TextType.CODE)
        html_node = text_node.to_html_node()
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), f"<code>a</code>")
    
    def test_link(self):
        text_node = TextNode("a", TextType.LINK, "b")
        html_node = text_node.to_html_node()
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), f"<a href=\"b\">a</a>")
    
    def test_bold(self):
        text_node = TextNode("a", TextType.IMAGE, "b")
        html_node = text_node.to_html_node()
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), f"<img alt=\"a\" src=\"b\"></img>")