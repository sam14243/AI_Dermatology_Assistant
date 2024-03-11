from fastapi import APIRouter, Depends, HTTPException, Body, status, Header, Query
from typing import Optional, List
import json
from Schema.schema import ImageData
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import base64
from PIL import Image
from io import BytesIO
from connections.mongo_db import db_client
from datetime import datetime
import requests

router = APIRouter(
    prefix="/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')
    

@router.post("/")
async def save_image(data: ImageData = Body(..., description="Image data")):
    base64_data = data.image.replace('data:image/jpeg;base64,', '')
    image_bytes = base64.b64decode(base64_data)

    image = Image.open(BytesIO(image_bytes))

    image_filename = f"{data.userid}_image.jpg"
    image_path = f"images/{image_filename}"
    image.save(image_path)
    print("image_saved")
    db_client.update_user_data(data.userid, {"image_path": image_path})
    
    try:
        
        response = requests.post("https://c020-115-244-132-22.ngrok-free.app/hehe", data = json.dumps({"image":encode_image_to_base64(image_path)}))
        
        if response.status_code == 202:
            response_data = eval(response.content.decode('utf-8'))
            print(response_data, type(response_data))
            # response_data = {'0': ['Acne', 'bcc', 'malignant', 'Tinea Ringworm Candidiasis and other Fungal Infections'], '1': ['Papular', 'bkl', 'benign', 'Eczema']}
            # start_room(str(data.userid)+"1234")
            db_client.update_user_data(data.userid, {"diagnosis": response_data})
            
            # return "Hello jkaps"
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=response_data)
        
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch image")
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
    # return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Image saved successfully.", "image_path": image_path})
