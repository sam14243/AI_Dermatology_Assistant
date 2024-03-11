from fastapi import APIRouter, Depends, HTTPException, Body, status, Header, Query
from typing import Optional, List
import json
from Schema.schema import DBData
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import base64
from connections.mongo_db import db_client

router = APIRouter(
    prefix="/db",
    tags=["db"],
    responses={404: {"description": "Not found"}},
)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')

@router.post("/del")
async def analyse_disease(data: DBData = Body(..., description="analyse data")):
    try:
        print(data.userid,str(data.userid)+"1234")
        db_client.delete_documents_by_userid(data.userid)
        db_client.delete_documents_by_roomid(str(data.userid)+"1234")
        print("delete done")
    except Exception as e:
        print(e)
    response = {"message":"del done"}
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=response)

@router.post("/ret")
async def analyse_disease(data: DBData = Body(..., description="analyse data")):
    try:
        t1 = db_client.get_user_data(data.userid)
        print(t1)
        t2 = db_client.get_user_room(str(data.userid)+"1234")
        print(t2)
    except Exception as e:
        print(e)
    response = {"message":"ret done"}
    return "checked"