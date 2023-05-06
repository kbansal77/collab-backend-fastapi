def postEntry(item) -> (dict):
    return{
        "id": str(item["_id"]),
        "title":item["title"],
        "cover": item["cover"],
        "deadline": item["deadline"],
        "batch": item["batch"],
        "tech_stack": item["tech_stack"],
        "college": item["college"],
        "team_size": item["team_size"],
        "project_description": item["project_description"],
        "role_name": item["role_name"],
        "role_description": item["role_description"],
        "post_type": item["post_type"],
        "document_link": item["document_link"],
        "internship_start_date": item["internship_start_date"],
        "internship_duration": item["internship_duration"],
        "internship_venue": item["internship_venue"],
        "internship_stipend": item["internship_stipend"],
        "job_offer": item["job_offer"],
        "hackathon_starting_date": item["hackathon_starting_date"],
        "hackathon_duration": item["hackathon_duration"],
        "hackathon_website": item["hackathon_website"],
        "hackathon_venue": item["hackathon_venue"],
        "saved_by": item["saved_by"],
        "applied_by": item["applied_by"],
        "created_by": item["created_by"],
        "created_at": item["created_at"],
    }

def postsEntry(entries) -> (list):
    return [postEntry(item) for item in entries]