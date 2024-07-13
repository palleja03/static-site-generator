import unittest

from htmlnode import HTMLNode, LeafNode


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


    def test_leaf_node_no_value_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode(value=None, tag="p")

    def test_leaf_node_no_tag_to_html(self):
        leaf = LeafNode(tag = "p", value="This is a paragraph of text.")
        expected_result = "<p>This is a paragraph of text.</p>"
        self.assertEqual(leaf.to_html(), expected_result)

    def test_leaf_node_to_html(self):
        leaf = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        expected_result = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(leaf.to_html(), expected_result)

    def test_leaf_node_no_value_raises_error(self):
        with self.assertRaises(ValueError) as context:
            LeafNode(tag="p", value=None)
            
        self.assertEqual(str(context.exception), "LeafNode requires a non-empty value.")