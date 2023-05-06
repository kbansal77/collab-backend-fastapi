from fastapi import APIRouter, HTTPException, Request, File, UploadFile
from models import User
from schema.user import userEnitry, usersEntiry
from schema.post import postEntry, postsEntry
from bson.objectid import ObjectId
from fastapi.responses import FileResponse
import shutil
import uuid

from config.db import conn

user = APIRouter()

@user.get('/')
async def find_all_user():
    try:
        return usersEntiry(conn["collab"]["users"].find())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@user.get('/{userEmail}')
async def find_user(userEmail:str):
    try:
        print(conn["collab"]["users"].find_one({"email":userEmail}))
        userData = userEnitry(conn["collab"]["users"].find_one({"email":userEmail}))
        postsCreatedData = postsEntry(conn["collab"]["posts"].find({"created_by": userEmail}))
        if(len(postsCreatedData)):
            userData["posts_created"] = postsCreatedData
        response = []
        if len(userData["posts_saved"]):
            postsSaved = userData["posts_saved"]
            for postid in postsSaved:
                temp = postEntry(conn["collab"]["posts"].find_one({"_id": ObjectId(postid)}))
                response.append(temp)
        userData["posts_saved"] = response
        response = []
        if len(userData["posts_applied"]):
            for postid in userData["posts_applied"]:
                temp = postEntry(conn["collab"]["posts"].find_one({"_id": ObjectId(postid)}))
                response.append(temp)
        userData["posts_applied"] = response
        return userData
        # return userEnitry(conn["collab"]["users"].find_one({"email":userEmail}))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))  

@user.post('/')
async def create_user(user: User):
    try:
        newUser = conn["collab"]["users"].insert_one(dict(user))
        return userEnitry(conn["collab"]["users"].find_one({"_id": newUser.inserted_id})) 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@user.put('/{emailid}')
async def update_user(emailid:str, user:User):
    try:
        print(emailid)
        conn["collab"]["users"].update_one({"email":emailid},{
            "$set": dict(user)
        })
        return userEnitry(conn["collab"]["users"].find_one({"email":emailid}))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
@user.get('/created/{userEmail}')
def get_posts_created(userEmail:str):
    try:
        return postsEntry(conn["collab"]["posts"].find({"created_by": userEmail}))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
@user.get('/saved/{userEmail}')
def get_posts_saved(userEmail:str):
    try:
        userData = userEnitry(conn["collab"]["users"].find_one({"email":userEmail}))
        print(userData)
        if len(userData["posts_saved"]):
            postsSaved = userData["posts_saved"]
            response = []
            for postid in postsSaved:
                temp = postEntry(conn["collab"]["posts"].find_one({"_id": ObjectId(postid)}))
                response.append(temp)
            return response
        return []
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
@user.get('/applied/{userEmail}')
def get_posts_applied(userEmail:str):
    try:
        userData = userEnitry(conn["collab"]["users"].find_one({"email":userEmail}))
        postsApplied = userData["posts_applied"]
        if len(postsApplied):
            response = []
            for postid in postsApplied:
                temp = postEntry(conn["collab"]["posts"].find_one({"_id": ObjectId(postid)}))
                response.append(temp)
            return response
        return []
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
@user.post('/uploadResume/{email}')
def upload_resume(email:str, file: UploadFile = File(...)):
    try:
        print(file)
        filename = uuid.uuid4()
        with open("Resumes/{}.pdf".format(filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": filename,"email":email}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
