import unittest

from leafnode import LeafNode

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
