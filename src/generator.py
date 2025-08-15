import os
import pathlib

from markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print("Generating page from", from_path, "to", dest_path, "using template", template_path)
    content = pathlib.Path(from_path).read_text()
    template = pathlib.Path(template_path).read_text()
    html = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    template = template.replace("{{ Content }}", html).replace("{{ Title }}", title)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    output = pathlib.Path(dest_path)
    if not output.parent.exists():
        output.parent.mkdir(parents=True)
    output.write_text(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = pathlib.Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


# def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
#     for path in pathlib.Path(dir_path_content).rglob("*.md"):
#         relative_path = path.relative_to(dir_path_content)
#         dest_path = pathlib.Path(dest_dir_path) / relative_path.with_suffix(".html")
#         generate_page(path, template_path, dest_path)