from fastapi import APIRouter, Depends, HTTPException, Body, status, Header, Query
from typing import Optional, List
import json
from Schema.schema import SymptomData
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from connections.mongo_db import db_client

router = APIRouter(
    prefix="/symptoms",
    tags=["symptoms"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def save_symptoms(data: SymptomData = Body(..., description="Image data")):
    response = data.dict()
    for i in response:
        if len(response[i]) > 0 and i!="userid":
            db_client.update_user_data(data.userid, {i: response[i]})
    print(data, type(data))
    
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "data saved successfully."})