import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_null_node(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_tag_set(self):
        v = "test"
        node = HTMLNode(tag=v)
        self.assertEqual(node.tag, v)
    
    def test_value_set(self):
        v = "test"
        node = HTMLNode(value=v)
        self.assertEqual(node.value, v)

    def test_children_set(self):
        v = "test"
        node = HTMLNode(children=v)
        self.assertEqual(node.children, v)
    
    def test_tag_set(self):
        v = "test"
        node = HTMLNode(props=v)
        self.assertEqual(node.props, v)
    
    def test_to_html(self):
        with self.assertRaises(NotImplementedError):
            node = HTMLNode()
            node.to_html()
    
    def test_props_to_html(self):
        node1 = HTMLNode()
        self.assertEqual(node1.props_to_html(), "")
        node2 = HTMLNode(props={"a": 1, "b": 2})
        self.assertEqual(node2.props_to_html(), " a=\"1\" b=\"2\"")
    