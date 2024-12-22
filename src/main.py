import os, shutil

from textnode import TextNode, TextType
from util import extract_title, markdown_to_html_node

def copy_source_destination(source="static", destination="public"):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    items = os.listdir(source)
    if not items:
        return
    
    for item in items:
        item_path_source = os.path.join(source, item)
        item_path_destination = os.path.join(destination, item)
        if os.path.isfile(item_path_source):
            shutil.copy(item_path_source, item_path_destination)
        else:
            copy_source_destination(item_path_source, item_path_destination)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as markdown_file:
        markdown = markdown_file.read()
    with open(template_path, "r") as template_file:
        template = template_file.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as dest_file:
        dest_file.write(html)

def main():
    print(TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev"))
    copy_source_destination(
        os.path.join(os.path.curdir, "static"), 
        os.path.join(os.path.curdir, "public")
    )
    generate_page("content/index.md", "template.html", "public/index.html")
    
if __name__ == '__main__':
    main()
