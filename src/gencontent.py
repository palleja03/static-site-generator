from markdown_blocks import markdown_to_blocks, markdown_to_html_node
import os

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    with open(template_path, "r") as f:
        template = f.read()
    
    new_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as f:
        f.write(new_html)

if __name__ == "__main__":
    print(os.path.exists("./el_nabo/peludo/index.html"))
    print(generate_page("./content/index.md", "./template.html", "./el_nabo/peludo/index.html"))