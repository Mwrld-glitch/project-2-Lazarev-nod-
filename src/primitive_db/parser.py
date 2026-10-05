def parse_where(tokens):
    """Разбирает условие WHERE. Возвращает словарь или None при ошибке."""
    if len(tokens) != 3 or tokens[1] != "=":
        return None
    key = tokens[0]
    value = _convert(tokens[2])
    return {key: value}


def parse_set(tokens):
    """Разбирает условие SET. Возвращает словарь или None при ошибке."""
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