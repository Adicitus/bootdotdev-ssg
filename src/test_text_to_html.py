import unittest
import unittest

from text_to_html import text_node_to_html_node
from leafnode import LeafNode
from textnode import TextNode, TextType


class TestTextToHTML(unittest.TestCase):
    def test_plaintext(self):
        text_node = TextNode("a", TextType.PLAIN)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.to_html(), text_node.text)
    
    def test_bold(self):
        text_node = TextNode("a", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), f"<b>a</b>")
    
    def test_italic(self):
        text_node = TextNode("a", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), f"<i>a</i>")
    
    def test_code(self):
        text_node = TextNode("a", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), f"<code>a</code>")
    
    def test_link(self):
        text_node = TextNode("a", TextType.LINK, "b")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), f"<a href=\"b\">a</a>")
    
    def test_bold(self):
        text_node = TextNode("a", TextType.IMAGE, "b")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), f"<img alt=\"a\" src=\"b\"></img>")
