import re
from htmlnode import HTMLNode,LeafNode, ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes
from functools import reduce


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = [block.strip() for block in blocks if block != ""]
    return filtered_blocks

def block_to_block_type(block):
    block_lines = block.split("\n")
    lines_quote_map = map(lambda line: re.match(r"^>", line), block_lines)
    lines_unordered_list_map = map(lambda line: re.match(r"^\* |^- ", line), block_lines)
    ordered_numbers = list(map(lambda x: str(x), range(1,len(block_lines) + 1)))
    lines_ordered_list_tuples = list(map(lambda line: (line[0], re.match(r"^\d{1}\. ", line)), block_lines))
    zipped_ordered_tuples = zip(ordered_numbers, lines_ordered_list_tuples)
    lines_ordered_map = map(lambda row: row[0] == row[1][0] and row[1][1], zipped_ordered_tuples)
    
    if re.match(r"^#{1,6} ", block_lines[0]):
        return block_type_heading
    elif re.match(r"^```[\s\S]*```$", block, re.MULTILINE):
        return block_type_code
    elif reduce(lambda a,b: a and b, lines_quote_map):
        return block_type_quote
    elif reduce(lambda a,b: a and b, lines_unordered_list_map):
        return block_type_ulist
    elif reduce(lambda a,b: a and b, lines_ordered_map):
        return block_type_olist
    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def text_to_children(text):
    return list(map(text_node_to_html_node,text_to_textnodes(text)))


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")





def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)