from collections import defaultdict

def uppercase_values(obj):
    """
    Recursively convert all string values in a dict or list to uppercase.

    Args:
        obj: dict, list, or single value

    Returns:
        obj with all string values converted to uppercase
    """
    if isinstance(obj, dict):
        return {k: uppercase_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [uppercase_values(item) for item in obj]
    elif isinstance(obj, str):
        return obj.upper()
    else:
        return obj

def build_permission_tree(mappings):
    """
    mappings: iterable with fields:
    - role_code (nullable)
    - app_code
    - page_code
    - permission_id
    """

    tree = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(set)
        )
    )

    for m in mappings:
        tree[m["role_key"]][m["app"]][m["page"]].add(m["permission"])

    return tree
