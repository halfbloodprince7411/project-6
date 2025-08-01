def get_students():
    return [
        {"id": 1, "name": "Alice", "age": 20},
        {"id": 2, "name": "Bob", "age": 22},
        {"id": 3, "name": "Charlie", "age": 19},
    ]

def get_teachers():
    from flask import session
    user = session.get("user")
    
    if user and user.get("preferred_username") == "teacher01@pemmrajusirishaoutlook.onmicrosoft.com":
        return [{
            "name": user.get("name"),
            "email": user.get("preferred_username")
        }]
    
    return []

