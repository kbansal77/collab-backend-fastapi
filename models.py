from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Literal
from pydantic import AnyUrl, EmailStr, Field
import uuid

class User(BaseModel):
    # id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: Optional[str]
    photoURL: Optional[str]
    posts_created: Optional[List[str]]
    posts_applied: Optional[List[str]]
    posts_saved: Optional[List[str]]
    email:Optional[str]
    graduating_year:Optional[str]
    degree: Optional[str]
    github: Optional[str]
    college: Optional[str]
    resume: Optional[str]
    linkedin: Optional[str]
    blogs:Optional[str]
    website:Optional[str]
    describe:Optional[str]

class Post(BaseModel):
    # id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title:Optional[str]
    cover: Optional[str]
    deadline: Optional[str]
    batch: Optional[List[str]]
    tech_stack: Optional[List[str]]
    college: Optional[str]
    team_size: Optional[int]
    project_description: Optional[str]
    role_name: Optional[str]
    role_description: Optional[str]
    post_type: Optional[Literal["Project", "Internship", "Hackathon"]]
    document_link: Optional[str]
    internship_start_date: Optional[datetime]
    internship_duration: Optional[int]
    internship_venue: Optional[str]
    internship_stipend: Optional[str]
    job_offer:Optional[str]
    hackathon_starting_date: Optional[datetime]
    hackathon_duration: Optional[int]
    hackathon_website: Optional[str]
    hackathon_venue:Optional[str]
    saved_by:Optional[List[str]]
    applied_by:Optional[List[str]]
    created_by: Optional[str]
    created_at: Optional[datetime]
