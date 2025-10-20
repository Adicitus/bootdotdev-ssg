import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node1 = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node1.to_html()
        
        v2 = "testvalue"
        node2 = LeafNode(None, v2)
        self.assertEqual(node2.to_html(), v2)

        v3 = "a", "anchor", {"href": "http://localhost"}
        node3 = LeafNode(*v3)
        self.assertEqual(node3.to_html(), f"<{v3[0]}{node3.props_to_html()}>{v3[1]}</{v3[0]}>")

class TestParentNode(unittest.TestCase):
    def test_null_values(self):
        node1 = ParentNode(None, None)
        with self.assertRaises(ValueError): node1.to_html()
        node2 = ParentNode("tag", None)
        with self.assertRaises(ValueError): node2.to_html()
    
    def test_to_html(self):
        v = (
            "parent",
            [LeafNode("p", "child")]
        )
        node = ParentNode(*v)

        self.assertEqual(node.to_html(), f"<{node.tag}>{node.children[0].to_html()}</{node.tag}>")
    
    def test_find_tag(self):
        child_node1 = LeafNode("h1", "child1")
        child_node2 = LeafNode("p", "child2")
        child_node3 = LeafNode("p", "child3")
        parent_node = ParentNode("parent", [child_node1, child_node2, child_node3])
        grandparent_node = ParentNode("parent", [parent_node])

        
        self.assertListEqual(parent_node.find_tag("h1"), [child_node1])
        self.assertListEqual(parent_node.find_tag("p"), [child_node2, child_node3])
        self.assertListEqual(parent_node.find_tag("p", 1), [child_node2])
        self.assertListEqual(grandparent_node.find_tag("parent"), [grandparent_node, parent_node])
        self.assertListEqual(grandparent_node.find_tag("parent", 1), [grandparent_node])