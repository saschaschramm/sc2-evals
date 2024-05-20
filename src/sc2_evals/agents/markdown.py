def code(language: str, text: str) -> str:
    return f"```{language}\n{text}\n```\n"

def headline(text: str) -> str:
    return f"## {text}\n"

def strong(text: str) -> str:
    return f"**{text}**  \n"