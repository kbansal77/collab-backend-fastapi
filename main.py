from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from routes.user import user
from routes.post import post
# from routers import post, course, chapter, user, badge, bookmark, notification
# from firebase_admin import auth

tags_metadata = [
    {
        "name": "Post",
        "description": "Endpoints related to operations on the **Posts**\
            collection."
    },
    {
        "name": "User",
        "description": "Endpoints related to operations on the **Users**\
            collection."
    }
]

app = FastAPI(
    title="Collab Backend",
    description="Backend for the Collab Web App",
    version="1.0",
    openapi_tags=tags_metadata
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(exc)
    return Response(status_code=422, content=str(exc))


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(exc)
    return Response(status_code=exc.status_code, content=exc.detail)


app.include_router(
    post,
    prefix="/post",
    tags=["Post"]
)

# app.include_router(
#     course.router,
#     prefix="/course",
#     tags=["Course"]
# )

# app.include_router(
#     chapter.router,
#     prefix="/chapter",
#     tags=["Chapter"]
# )

app.include_router(
    user,
    prefix="/user",
    tags=["User"]
)

# app.include_router(
#     badge.router,
#     prefix="/badge",
#     tags=["Badge"]
# )

# app.include_router(
#     bookmark.router,
#     prefix="/bookmark",
#     tags=["Bookmark"]
# )

# app.include_router(
#     notification.router,
#     prefix="/notification",
#     tags=["Notification"]
# )
