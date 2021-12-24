def to_json(data: dict)-> dict:
    """
    All this does it add a ":" to the keys.
    """
    return {f":{key}": value for key, value in data.items()}