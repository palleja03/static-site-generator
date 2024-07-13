import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq_with_no_prop(self):
        node = HTMLNode("p", "This is a HTML paragraph")
        node2 = HTMLNode(tag = "p", value = "This is a HTML paragraph")
        self.assertEqual(node, node2)

    def test_eq_with_no_value(self):
        prop = {
                "href": "https://www.google.com", 
                "target": "_blank",
            }
        child = HTMLNode("p", "This is a HTML paragraph")
        node = HTMLNode(tag = "p", children = [child], props=prop)
        node2 = HTMLNode(tag = "p", children = [child], props=prop)
        self.assertEqual(node, node2)

    def test_eq_on_children(self):
        prop = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }
        child = HTMLNode("p", "This is a HTML paragraph")
        child2 = HTMLNode("p", "This is a HTML paragraph")
        node = HTMLNode(tag = "p", children = [child], props=prop)
        node2 = HTMLNode(tag = "p", children = [child2], props=prop)
        self.assertEqual(node, node2)

class TestLeafNode(unittest.TestCase): 
    def test_eq(self):
        leaf = LeafNode(tag = "a", value = "Click me!", props={"href": "https://www.google.com"})
        leaf2 = LeafNode(tag = "a", value = "Click me!", props = {"href": "https://www.google.com"})
        self.assertEqual(leaf, leaf2)

    def test_eq_no_prop(self):
        leaf = LeafNode(tag = "p", value="This is a paragraph of text.")
        leaf2 = LeafNode(tag="p", value="This is a paragraph of text.")
        self.assertEqual(leaf, leaf2)

    def test_leaf_node_no_tag_to_html(self):
        leaf = LeafNode(tag = "p", value="This is a paragraph of text.")
        expected_result = "<p>This is a paragraph of text.</p>"
        self.assertEqual(leaf.to_html(), expected_result)

    def test_leaf_node_to_html(self):
        leaf = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        expected_result = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(leaf.to_html(), expected_result)

    def test_leaf_node_no_value_to_html(self):
        with self.assertRaises(ValueError) as context:
            LeafNode(tag="p", value=None).to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no value")


class TestParentNode(unittest.TestCase): 
    def test_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        node2 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node, node2)

    def test_non_nested_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        expected_result = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_result)

    def test_nested_to_html(self):
        inner_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        parent = ParentNode(
            "p",
            [
                LeafNode("b", "Begin:"),
                inner_node,
                LeafNode("i", "end.")
            ]

        )
        inner_node_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        expected_result = f"<p><b>Begin:</b>{inner_node_html}<i>end.</i></p>"

        self.assertEqual(parent.to_html(), expected_result)

    def test_props_in_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"href": "https://www.google.com"}
        )
        expected_result = """<p href="https://www.google.com"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"""
        self.assertEqual(node.to_html(), expected_result)

    def test_no_tag_to_html(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [LeafNode("b", "Bold text"),]).to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no tag")

if __name__ == "__main__":
    unittest.main()