from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DOCUMENTS_DIR = SCRIPT_DIR / "documents"

def show_folder_contents(folder: Path) -> None:
    if folder.exists():
        for item in folder.iterdir():
            if item.is_file():
                print(f"{item.name} (file, {item.stat().st_size} bytes)")
            elif item.is_dir():
                print(f"{item.name} (folder)")
    else:
        print("No such folder path exists")

def find_files_by_extension(folder: Path, extension: str) -> list[Path]:
    if not folder.exists():
        print("No such folder path exists")
        return []

    list_paths = []

    for file in folder.rglob(f"*{extension}"):
        list_paths.append(file.absolute())
    return list_paths
    
def read_file_summary(file_path: Path) -> str:
    """Return the character and line count for a text file."""

    if not file_path.is_file():
        return f"{file_path.name}: not a valid file"

    content = file_path.read_text()

    character_count = len(content)

    lines = content.splitlines()

    line_count = len(lines)

    return (
        f"{file_path.name}: "
        f"{character_count} characters, "
        f"{line_count} lines"
    )

def main():
    print("Contents of documents folder:")
    show_folder_contents(DOCUMENTS_DIR)
    print("All .txt files in the tree:")
    list_all_files = find_files_by_extension(DOCUMENTS_DIR, ".txt")
    if not list_all_files:
            print(f"No file with extension .txt found")
    else:
        for file in list_all_files:
            print(file)
    print("Summary of notes.txt:")
    print(read_file_summary(DOCUMENTS_DIR / "notes.txt"))
    print("Summary of nonexistent.txt:")
    print(read_file_summary(DOCUMENTS_DIR / "nonexistent.txt"))




if __name__ == "__main__":
    main()
