def write_file(file_path: str, string: str) -> None:
    with open(file=file_path, mode="a", encoding="utf-8") as file:
        file.write(string)
