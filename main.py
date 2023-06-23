from fastapi import FastAPI
from routers import blog
from database import Base, engine, SessionLocal



app = FastAPI()
Base.metadata.create_all(bind = engine)

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()


# include routers
app.include_router(blog.router)

# include exceptions



    
    