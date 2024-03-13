from fastapi.middleware.cors import CORSMiddleware
# Use a pipeline as a high-level helper

import cv2 as cv
import numpy as np
from Schema.schema import ImageData
from CVModel.model import visual_adapters
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Body, status, Header, Query
from typing import Optional, List
import json
from Schema.schema import ImageData
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import base64
from PIL import Image
from io import BytesIO


print("Model?")
model = visual_adapters()
print("Done ig...")
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(image_api.router)
# app.include_router(symptoms_api.router)
# app.include_router(analyse_api.router)
# app.include_router(chat_api.router)

@app.get("/")
async def root():
    return {"message": "Initialized the server successfully!"}

@app.get("/model1")
async def mod1(data: ImageData = Body(..., description="Image data")):
    base64_data = data.image.replace('data:image/jpeg;base64,', '')
    image_bytes = base64.b64decode(base64_data)

    image = Image.open(BytesIO(image_bytes))
    cv.imshow('hehehe',image)
    print(type(image))
    print(image.shape)
    # response = funct1()
    
    return {"message": "Initialized the server successfully....!"}



@app.post("/hehe")
async def save_image(data: ImageData = Body(..., description="Image data")):
    base64_data = data.image.replace('data:image/jpeg;base64,', '')
    image_bytes = base64.b64decode(base64_data)

    image = Image.open(BytesIO(image_bytes))
    print(type(image))
    z = model(image)
    print(z)
    # cv.imshow("drjni",image)
    # db_client.update_user_data(data.userid, {"image_path": image_path})
    
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED,content=z)