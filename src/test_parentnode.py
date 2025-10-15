import unittest
from src.leafnode import LeafNode

from parentnode import ParentNode

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

    