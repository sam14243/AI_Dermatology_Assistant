from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API import db_api, image_api, symptoms_api, chat_api

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image_api.router)
app.include_router(symptoms_api.router)
app.include_router(db_api.router)
app.include_router(chat_api.router)

@app.get("/")
async def root():
    return {"message": "Initialized the server successfully!"}