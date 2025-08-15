import unittest

from htmlnode import HTMLNode, LeafNode
from markdown import markdown_to_html_node, extract_title


class TestMarkdown(unittest.TestCase):
    def test_emptiness(self):
        html = markdown_to_html_node("")
        self.assertIsInstance(html, HTMLNode)
        self.assertEqual(html.tag, "div")
        self.assertEqual(len(html.children), 0)
        self.assertEqual(html.value, None)
        self.assertEqual(html.props, None)

    def test_heading(self):
        html = markdown_to_html_node("# Title")
        self.assertIsInstance(html, HTMLNode)
        self.assertEqual(html.tag, "div")
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].tag, "h1")
        self.assertEqual(html.children[0].value, None)
        self.assertEqual(html.children[0].props, None)
        self.assertEqual(html.value, None)
        self.assertEqual(html.props, None)
        self.assertEqual(html.to_html(), '<div><h1>Title</h1></div>')
        leaf = html.children[0].children[0]
        self.assertIsInstance(leaf, LeafNode)
        self.assertEqual(leaf.value, "Title")
        self.assertEqual(leaf.tag, None)
        self.assertEqual(leaf.children, None)
        self.assertEqual(leaf.props, None)
        self.assertEqual(leaf.to_html(), "Title")

    def test_paragraph(self):
        html = markdown_to_html_node("This is a paragraph.")
        self.assertIsInstance(html, HTMLNode)
        self.assertEqual(html.tag, "div")
        self.assertEqual(len(html.children), 1)
        self.assertEqual(html.children[0].tag, "p")
        self.assertEqual(html.children[0].value, None)
        self.assertEqual(html.children[0].props, None)
        self.assertEqual(html.value, None)
        self.assertEqual(html.props, None)
        self.assertEqual(html.to_html(), '<div><p>This is a paragraph.</p></div>')
        leaf = html.children[0].children[0]
        self.assertIsInstance(leaf, LeafNode)
        self.assertEqual(leaf.value, "This is a paragraph.")
        self.assertEqual(leaf.tag, None)
        self.assertEqual(leaf.children, None)
        self.assertEqual(leaf.props, None)
        self.assertEqual(leaf.to_html(), "This is a paragraph.")

    def test_heading_paragraph(self):
        markdown = "# Heading\n\nThis is a paragraph."
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, HTMLNode)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(html_node.value, None)
        self.assertEqual(len(html_node.children), 2)
        heading = html_node.children[0]
        self.assertEqual(heading.tag, "h1")
        self.assertEqual(heading.value, None)
        self.assertEqual(len(heading.children), 1)
        paragraph = html_node.children[1]
        self.assertEqual(paragraph.tag, "p")
        self.assertEqual(paragraph.value, None)
        self.assertEqual(len(paragraph.children), 1)
        self.assertEqual(html_node.to_html(), "<div><h1>Heading</h1><p>This is a paragraph.</p></div>")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> with multiple lines   
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nwith multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_extract_title(self):
        md = """
# Main Title

This is a paragraph.
"""
        title = extract_title(md)
        self.assertEqual(title, "Main Title")

    def test_extract_title_no_heading(self):
        md = """
This is a paragraph."""

        with self.assertRaises(ValueError):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()
