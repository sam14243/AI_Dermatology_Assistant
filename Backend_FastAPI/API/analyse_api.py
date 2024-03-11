from fastapi import APIRouter, Depends, HTTPException, Body, status, Header, Query
from typing import Optional, List
import json
from Schema.schema import AnalyseData
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/analyse",
    tags=["analyse"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def analyse_disease(data: AnalyseData = Body(..., description="analyse data")):
    response = data
    
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=response)