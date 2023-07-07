from fastapi import FastAPI, Response
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

from routers import blog, auth
from database import Base, engine





app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Assuming your frontend runs on port 3000
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)



# include routers
app.include_router(blog.router)
app.include_router(auth.router)
Base.metadata.create_all(bind=engine)

# include exceptions


