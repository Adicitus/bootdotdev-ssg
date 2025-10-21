import sys
import os
import shutil
from generate_page import generate_page

from textnode import TextNode, TextType

def main(basepath="/", force_regen=False):
    node = TextNode(
        "This is some anchor text",
        TextType.LINK,
        "http://0.0.0.0:8888"
    )

    src_folder = os.path.dirname(__file__)
    project_folder  = os.path.abspath(os.path.join(src_folder, ".."))
    public_folder   = os.path.join(project_folder, "public", basepath.strip("/"))
    static_folder   = os.path.join(project_folder, "static")
    content_folder   = os.path.join(project_folder, "content")

    print(f"{project_folder}: {os.path.exists(project_folder)}")
    print(f"{public_folder}: {os.path.exists(public_folder)}")
    print(f"{static_folder}: {os.path.exists(static_folder)}")
    print(f"{content_folder}: {os.path.exists(static_folder)}")

    generate = not os.path.exists(public_folder) or (force_regen and os.path.isdir(public_folder))

    if generate and os.path.exists(public_folder):
        print(f"Removing existing public folder: {public_folder}")
        shutil.rmtree(public_folder)

    if generate:
        # Copy static assets
        def copy_files(src_root, dst_root):
            for item in os.scandir(src_root):
                if item.is_dir():
                    new_src_path = os.path.join(src_root, item.name)
                    new_dst_path = os.path.join(dst_root, item.name)
                    print(f"Creating new directory: {new_dst_path}")
                    os.mkdir(new_dst_path)
                    copy_files(new_src_path, new_dst_path)
                else:
                    src_path = os.path.join(src_root, item.name)
                    dst_path = os.path.join(dst_root, item.name)
                    print(f"Copying: {src_path} -> {dst_path}")
                    shutil.copy(src_path, dst_path)
        print(f"Creating public folder ({public_folder})")
        os.mkdir(public_folder)
        print("Copying static files...")
        copy_files(static_folder, public_folder)
        
        # Generate HTML
        def generate_pages(src_root, dst_root, template_path, basepath="/"):
             for item in os.scandir(src_root):
                if item.is_dir():
                    new_src_path = os.path.join(src_root, item.name)
                    new_dst_path = os.path.join(dst_root, item.name)
                    print(f"Creating new directory: {new_dst_path}")
                    os.mkdir(new_dst_path)
                    generate_pages(new_src_path, new_dst_path, template_path)
                else:
                    if not item.name.endswith('.md'):
                        continue
                    src_path = os.path.join(src_root, item.name)
                    dst_path = os.path.join(dst_root, item.name.replace(".md", ".html"))
                    print(f"Generating HTML: {src_path} -> {dst_path}")
                    generate_page(src_path, dst_path, template_path, basepath)

        generate_pages(content_folder, public_folder, os.path.join(project_folder, "template.html"), basepath)


if __name__ == "__main__":
    print(sys.argv)
    basepath = "/"
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        basepath = sys.argv[1]
    
    print(f"Using basepath: {basepath}")
    regenerate = "-f" in sys.argv or "--force" in sys.argv
    print(regenerate)
    main(basepath, force_regen=regenerate)

