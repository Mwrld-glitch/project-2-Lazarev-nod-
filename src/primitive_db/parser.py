def parse_where(tokens):
    """Превращает список вида ['age', '=', '28'] в словарь {'age': 28}."""
    if len(tokens) != 3 or tokens[1] != "=":
        return None
    key = tokens[0]
    value = _convert(tokens[2])
    return {key: value}


def parse_set(tokens):
    """Превращает список вида ['age', '=', '29'] в словарь {'age': 29}."""
    if len(tokens) != 3 or tokens[1] != "=":
        return None
    key = tokens[0]
    value = _convert(tokens[2])
    return {key: value}


def _convert(value):
    """Преобразует строку в int, bool или str."""
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    try:
        return int(value)
    except ValueError:
        return value