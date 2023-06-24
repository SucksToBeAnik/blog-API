from fastapi import FastAPI, Response
from fastapi.testclient import TestClient
from routers import blog, auth
from database import Base, engine


app = FastAPI()


# include routers
app.include_router(blog.router)
app.include_router(auth.router)
Base.metadata.create_all(bind=engine)

# include exceptions


