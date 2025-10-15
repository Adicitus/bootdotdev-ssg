import unittest

from textnode import TextNode, TextType

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