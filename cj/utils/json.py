def from_json(json: dict, obj):
    """
    Create a object from JSON.
        
    Params:
        - json(dict): The json (dict).
        - obj(object): The object to create.
        
    Returns:
        - object
    """
    # Get the keys
    keys = json.keys()
    values = [value for key in keys for value in json[key]]

    return obj(*values)


def to_json(data: dict)-> dict:
    """
    All this does it add a ":" to the keys.
    """
    return {f":{key}": value for key, value in data.items()}