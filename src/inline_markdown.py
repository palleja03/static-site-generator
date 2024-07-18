import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_single_node(node, matches, type):
    if len(matches) == 0:
        if node.text != "": 
            return [node]
        else:
            return []
        
    if type == text_type_image:
        leading_char = "!"
        match_node_type = text_type_image
    elif type == text_type_link:
        leading_char = ""
        match_node_type = text_type_link
        
    
    result = []
    splitted = node.text.split(f"{leading_char}[{matches[0][0]}]({matches[0][1]})")
    left_node = TextNode(splitted[0], node.text_type)
    match_node = TextNode(matches[0][0], match_node_type, matches[0][1])
    right_node = TextNode("".join(splitted[1:]), node.text_type)
    if left_node.text != "":
        result.append(left_node)
    result.append(match_node)
    return result + split_single_node(right_node, matches[1:], type)

def split_nodes_image(old_nodes):
    if len(old_nodes) == 0:
        return []
    matches = extract_markdown_images(old_nodes[0].text)
    first_node_splitted = split_single_node(old_nodes[0], matches, text_type_image)
    return first_node_splitted + split_nodes_link(old_nodes[1:])

def split_nodes_link(old_nodes):
    if len(old_nodes) == 0:
        return []
    matches = extract_markdown_links(old_nodes[0].text)
    first_node_splitted = split_single_node(old_nodes[0], matches, text_type_link)
    return first_node_splitted + split_nodes_link(old_nodes[1:])

def text_to_textnodes(text):
    current_nodes = [TextNode(text, text_type_text)]
    current_nodes = split_nodes_image(current_nodes)
    current_nodes = split_nodes_link(current_nodes)
    current_nodes = split_nodes_delimiter(current_nodes, "**", text_type_bold)
    current_nodes = split_nodes_delimiter(current_nodes, "*", text_type_italic)
    current_nodes = split_nodes_delimiter(current_nodes, "`", text_type_code)
    return current_nodes

if __name__ == "__main__":
    nodes = text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    for node in nodes:
        print(node)
    
    # text_type_bold,
    # text_type_italic,
    # text_type_code,