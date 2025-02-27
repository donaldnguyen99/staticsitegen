import os, shutil
import sys

from textnode import TextNode, TextType
from util import extract_title, markdown_to_html_node

def copy_source_destination(source="static", destination="public", verbose=False):
    if verbose: print(f"Copying {source} to {destination}")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    
    for item in os.listdir(source):
        item_path_source = os.path.join(source, item)
        item_path_destination = os.path.join(destination, item)
        if os.path.isfile(item_path_source):
            if verbose: print(f"Copying {item_path_source} to {item_path_destination}")
            shutil.copy(item_path_source, item_path_destination)
        else:
            copy_source_destination(item_path_source, item_path_destination, verbose)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as markdown_file:
        markdown = markdown_file.read()
    with open(template_path, "r") as template_file:
        template = template_file.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    html = html.replace("href=\"/", f"href=\"{basepath}")
    html = html.replace("src=\"/", f"src=\"{basepath}")
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as dest_file:
        dest_file.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item_path.endswith(".md"):
                generate_page(item_path, template_path, os.path.join(dest_dir_path, item).removesuffix(".md") + ".html", basepath)
        else:
            generate_pages_recursive(item_path, template_path, os.path.join(dest_dir_path, item), basepath)

def main():
    # print(TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev"))
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_source_destination(
        os.path.join(os.path.curdir, "static"), 
        os.path.join(os.path.curdir, "docs"),
        verbose=True
    )
    generate_pages_recursive("content", "template.html", "docs", basepath)
    
if __name__ == '__main__':
    main()
