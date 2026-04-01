import sys
import shutil
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from src.markdown import generate_page, generate_pages_recursive


def copy_static_content(from_dir: str, to_dir: str):
    from_dir_path = Path(from_dir)
    to_dir_path = Path(to_dir)
    for file in from_dir_path.rglob("*"):
        relative_path = file.relative_to(from_dir_path)
        if file.is_file():
            shutil.copyfile(file, to_dir_path / relative_path)
        if file.is_dir():
            (to_dir_path / relative_path).mkdir(parents=True, exist_ok=True)


def main():
    copy_static_content("static", "public")
    generate_pages_recursive("content", "template.html", "public")

print(main())