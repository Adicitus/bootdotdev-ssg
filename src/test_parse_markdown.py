import unittest
from textnode import TextNode, TextType
from parse_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link, split_nodes, text_to_textnodes, markdown_to_blocks

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

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

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

    def test_text_to_textnodes(self):
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

        blocks = markdown_to_blocks(t)
        print(blocks)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ],
            blocks
        )