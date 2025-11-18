import os
import shutil

from blocktype import (
    markdown_to_html_node,
    extract_title
)

def static_to_public(path):
    static_path = os.path.join(os.path.abspath(os.getcwd()),"static", path)
    public_path = os.path.join(os.path.abspath(os.getcwd()),"docs", path)
    contents = os.listdir(static_path)

    for content in contents:
        content_path = os.path.join(static_path, content)
        if os.path.isfile(content_path):
            shutil.copy(os.path.join(static_path, content), os.path.join(public_path, content))
        else:
            directory_path = os.path.join(public_path, content)
            os.mkdir(directory_path)
            static_to_public(os.path.join(path, content))
            

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(html_string)

    new_html = template.replace("{{ Title }}", title)
    new_html = new_html.replace("{{ Content }}", html_string)
    new_html = new_html.replace('href="', f'href="{base_path}"')
    new_html = new_html.replace('src="', f'src="{base_path}"')

    path = os.path.dirname(dest_path)
    os.makedirs(path, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(new_html)
    
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    contents = os.listdir(dir_path_content)

    for content in contents:
        current_path = os.path.join(dir_path_content, content)

        if os.path.isfile(current_path) and content.split(".")[-1] == "md":
            new_file_name = content.split(".")[0]
            new_file_name += ".html"
            new_dest_path = os.path.join(dest_dir_path, new_file_name)
            generate_page(current_path, template_path, new_dest_path, base_path)
        elif os.path.isdir:
            os.makedirs(dest_dir_path, exist_ok=True)
            generate_pages_recursive(current_path, template_path, os.path.join(dest_dir_path, content), base_path)
    
    
