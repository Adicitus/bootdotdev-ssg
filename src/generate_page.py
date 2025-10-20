import os

from blocknode import BlockNode, BlockType


def generate_page(src_path, dst_path, template_path):
    print(f"Generating page from '{src_path}' to '{dst_path}' using '{template_path}'")

    src_text = None
    try:
        with open(src_path, 'r') as f: src_text = f.read()
    except Exception as e:
        print(f"Failed to read src file: {e}")
        return
    
    template_text = None
    try:
        with open(template_path, 'r') as f: template_text = f.read()
    except Exception as e:
        print(f"Failed to read template file: {e}")
        return

    text_node = BlockNode(BlockType.SECTION, src_text)
    html_node = text_node.to_html_node()
    title_node = html_node.find_tag('h1', limit=1)
    title = title_node[0].children[0].value if len(title_node) > 0 else "Unknown title"

    page_content = template_text.replace("{{ Title }}", title).replace("{{ Content }}", html_node.to_html())

    try:
        with open(dst_path, 'w') as f: f.write(page_content)
    except Exception as e:
        print(f"Failed to write the content: {e}")
        return
    
    print("Generation complete.")
    

    
    