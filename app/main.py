from fastapi import FastAPI
from . import models
from .database import engine
from .router import interview, applicant, hr, auth, admin
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


origins = [
    "http://localhost:5173",      # The exact origin where your FastAPI app is served from
    "http://localhost",           # Any port on localhost
    "http://127.0.0.1:5173",      # Using loopback IP address
    "http://192.168.0.10:5173",   # An example with a specific local IP address
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(interview.router)
app.include_router(applicant.router)
app.include_router(hr.router)
app.include_router(admin.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"main": "message"}
