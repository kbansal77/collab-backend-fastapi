from fastapi import APIRouter, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from models import Post
from bson.objectid import ObjectId
from schema.post import postEntry, postsEntry
from schema.user import userEnitry

from config.db import conn

import textract
import docx2txt
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


post = APIRouter()

@post.get('/')
def get_all_posts():
    try:
        return postsEntry(conn["collab"]["posts"].find())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@post.get('/{postid}')
def get_post_by_ID(postid:str):
    try: 
        postData = postEntry(conn["collab"]["posts"].find_one({"_id": ObjectId(postid)}))
        userData = userEnitry(conn["collab"]["users"].find_one({"email":postData["created_by"]})) 
        postData["ownerData"] = {
            "name": userData["name"],
            "photoURL": userData["photoURL"],
            "email": userData["email"],
            "github": userData["github"],
            "college": userData["college"],
            "resume": userData["resume"],
            "linkedin": userData["linkedin"],
            "blogs": userData["blogs"],
            "website": userData["website"]
        }

        return postData
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
@post.post("/")
def create_post(postData:Post):
    try:
        newPost = conn["collab"]["posts"].insert_one(dict(postData))
        print(postData.created_by)
        userData = userEnitry(conn["collab"]["users"].find_one({"email":postData.created_by})) 
        postsCreated = userData["posts_created"]
        postsCreated.append(newPost.inserted_id)
        conn["collab"]["users"].update_one({"email":postData.created_by},{"$set": {"posts_created": postsCreated}})
        return postEntry(conn["collab"]["posts"].find_one({"_id": newPost.inserted_id}))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@post.put("/save/{postid}/{userEmail}")
def save_post(postid:str, userEmail: str):
    try:
        postData = postEntry(conn["collab"]["posts"].find_one({"_id": ObjectId(postid)}))
        savedBy = postData["saved_by"]
        userData = userEnitry(conn["collab"]["users"].find_one({"email":userEmail})) 
        postsSaved = userData["posts_saved"]
        print({"savedby": savedBy,"postssaved": postsSaved})
        print(userData["id"])
        if postid in postsSaved:
            print("remove")
            postsSaved.remove(postData["id"])
            savedBy.remove(userData["email"])
        else:
            print("append")
            postsSaved.append(postData["id"])
            savedBy.append(userData["email"])

        print({"savedby": savedBy,"postssaved": postsSaved})

        conn["collab"]["users"].update_one({"email": userEmail}, {"$set":{"posts_saved": postsSaved}})
        conn["collab"]["posts"].update_one({"_id": ObjectId(postid)}, {"$set":{"saved_by":savedBy}})
        return postEntry(conn["collab"]["posts"].find_one({"_id": ObjectId(postid)}))
    
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
@post.put("/apply/{postid}/{userEmail}")
def apply_post(postid:str, userEmail: str):
    try:
        postData = postEntry(conn["collab"]["posts"].find_one({"_id": ObjectId(postid)}))
        appliedBy = postData["applied_by"]
        userData = userEnitry(conn["collab"]["users"].find_one({"email":userEmail})) 
        postsApplied = userData["posts_applied"]
        # print({"savedby": appliedBy,"postssaved": postsApplied})
        print(userData["id"])
        if postid in postsApplied:
            print("remove")
            postsApplied.remove(postData["id"])
            appliedBy.remove(userData["email"])
        else:
            print("append")
            postsApplied.append(postData["id"])
            appliedBy.append(userData["email"])

        # print({"savedby": appliedBy,"postssaved": postsApplied})

        conn["collab"]["users"].update_one({"email": userEmail}, {"$set":{"posts_applied": postsApplied}})
        conn["collab"]["posts"].update_one({"_id": ObjectId(postid)}, {"$set":{"applied_by":appliedBy}})
        return postEntry(conn["collab"]["posts"].find_one({"_id": ObjectId(postid)}))
    
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    

@post.get('/{postid}/applicants')
def get_applicant_details(postid:str):
    try: 
        data = []
        postData = postEntry(conn["collab"]["posts"].find_one({"_id": ObjectId(postid)}))
        job_description = " ".join(postData["tech_stack"])
        job_description = " ".join((job_description, postData["project_description"]))
        job_description = " ".join((job_description, postData["role_name"]))
        job_description= " ".join((job_description,postData["role_description"]))
        # for tech_stack in postData["tech_stack"]:
        # print(job_description)
            
        if len(postData["applied_by"]):
            for applicant in postData["applied_by"]:
                # userData={}
                userData = userEnitry(conn["collab"]["users"].find_one({"email":applicant}))
                data.append(userData)
            for applicant in data:
                resume = ""
                # resume = docx2txt.process('Resumes/{}.pdf'.format(applicant["resume"]))
                # print(resume)
                
                resume = textract.process('Resumes/{}.pdf'.format(applicant["resume"]))
                str(resume)
                # print(str(resume))
                resume = resume.decode("utf-8")
                # resume = resume.replace("\n"," ") 
                
                stop_words = set(stopwords.words('english'))
  
                word_tokens = word_tokenize(resume)
                jd_tokens = word_tokenize(job_description)

                resume = ' '.join(word_tokens)
                # print(resume)
                job = ' '.join(jd_tokens)
                text = [resume,job]
                cv = CountVectorizer()
                count_matrix = cv.fit_transform(text)
                print('Similarity score : ',cosine_similarity(count_matrix))
                #print similarity score
                matchpercentage = cosine_similarity(count_matrix)[0][1]
                matchpercentage = round(matchpercentage*100,2)
                print('Your Resume {} % match to the job description !'.format(matchpercentage))
                applicant["match"] = str(matchpercentage)


        return data
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
