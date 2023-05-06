def userEnitry(item) -> (dict):
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "photoURL": item["photoURL"],
        "posts_created": item["posts_created"],
        "posts_applied": item["posts_applied"],
        "posts_saved": item["posts_saved"],
        "email":item["email"],
        "graduating_year":item["graduating_year"],
        "degree": item["degree"],
        "github": item["github"],
        "college": item["college"],
        "resume": item["resume"],
        "linkedin": item["linkedin"],
        "blogs":item["blogs"],
        "website":item["website"],
        "describe":item["describe"]
    }

def usersEntiry(entity) -> list:
    return [userEnitry(item) for item in entity]