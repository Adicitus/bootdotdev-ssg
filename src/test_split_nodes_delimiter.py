import unittest
from textnode import TextNode, TextType
from parse_markdown import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_indivisible(self):
        node = TextNode("Test", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertIsInstance(new_nodes, list)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)
    
    def test_needle_at_tail(self):
        node = TextNode("Test `code`", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertIsInstance(new_nodes, list)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(f"{new_nodes[0].text}`{new_nodes[1].text}`", node.text)
        self.assertEqual(new_nodes[0].text_type, node.text_type)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
    
    def test_needle_at_head(self):
        node = TextNode("`code` test", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertIsInstance(new_nodes, list)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(f"`{new_nodes[0].text}`{new_nodes[1].text}", node.text)
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text_type, node.text_type)
    
    def test_needle_in_the_middle(self):
        node = TextNode("Test `code` test", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertIsInstance(new_nodes, list)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(f"{new_nodes[0].text}`{new_nodes[1].text}`{new_nodes[2].text}", node.text)
        self.assertEqual(new_nodes[0].text_type, node.text_type)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, node.text_type)

    def test_multiple_needles(self):
        node = TextNode("Test `code` test `code`", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertIsInstance(new_nodes, list)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(f"{new_nodes[0].text}`{new_nodes[1].text}`{new_nodes[2].text}`{new_nodes[3].text}`", node.text)
        self.assertEqual(new_nodes[0].text_type, node.text_type)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, node.text_type)
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

