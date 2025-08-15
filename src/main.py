import os
import shutil
import sys

from generator import generate_pages_recursive


def recursive_copy(src, dst):
    if os.path.exists(dst):
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        else:
            os.remove(dst)

    if not os.path.exists(src):
        raise FileNotFoundError(f"Source path '{src}' does not exist.")

    if os.path.isdir(src):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            recursive_copy(os.path.join(src, item), os.path.join(dst, item))
    else:
        shutil.copy2(src, dst)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    recursive_copy("static", "docs")
    generate_pages_recursive("./content/", "template.html", "./docs/", basepath)

if __name__ == "__main__":
    main()
