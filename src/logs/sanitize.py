def sanitize(info:dict) -> dict:
    sanitize_keys = [
        'token', 
        'access_token', 
        'refresh_token'
        ]
    new_dict = {}
    for key, value in info.items():
        if key in sanitize_keys:
            new_dict[key] = "[PRIVATE]"
            continue
        new_dict[key] = value
    return new_dict