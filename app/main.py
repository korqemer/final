from fastapi import FastAPI
from . import models
from .database import engine
from .router import interview, applicant, hr, auth


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(interview.router)
app.include_router(applicant.router)
app.include_router(hr.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"main": "message"}
