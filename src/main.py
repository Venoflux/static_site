import os
import shutil

import copy_static


def main():
    abs_path = os.path.abspath(os.getcwd())
    listdir = os.listdir(os.path.abspath(os.getcwd()))

    if "public" in listdir:
        print("Deleting public directory...")
        shutil.rmtree("./public")

    if "static" not in listdir:
        raise Exception("static file not found")
    
    print("Creating public directory...")
    public_path = os.path.join(abs_path, "public")
    os.mkdir(public_path)

    copy_static.static_to_public("")

    # Generate files
    copy_static.generate_pages_recursive(
        os.path.join(abs_path, "content"),
        os.path.join(abs_path, "template.html"),
        os.path.join(abs_path, "public")
    )
 

if __name__ == "__main__":
    main()
