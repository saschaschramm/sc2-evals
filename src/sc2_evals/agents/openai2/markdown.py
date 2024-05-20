def code(language: str, text: str) -> str:
    return f"```{language}\n{text}\n```\n"

def headline(level: int, text: str) -> str:
    level_str: str = "#" * level
    return f"{level_str} {text}\n"

def strong(text: str) -> str:
    return f"**{text}**  \n"