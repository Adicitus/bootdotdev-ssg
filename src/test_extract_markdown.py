import unittest

from parse_markdown import extract_markdown_images, extract_markdown_links

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        images = extract_markdown_images("t1 ![a](u1) t2 ![b](u2)")
        self.assertEqual(images[0], ("a", "u1"))
        self.assertEqual(images[1], ("b", "u2"))
    
    def test_extract_markdown_links(self):
        images = extract_markdown_links("t1 [a](u1) t2 ![b](u2)")
        self.assertEqual(images[0], ("a", "u1"))
        self.assertEqual(images[1], ("b", "u2"))
