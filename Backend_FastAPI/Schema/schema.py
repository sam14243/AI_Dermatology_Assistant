from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union

class ImageData(BaseModel):
    userid: Optional[str] = Field("", description="user id")
    image: Optional[str] = Field("", description="Base64 encoded image data")

    
class SymptomData(BaseModel):
    userid: Optional[str] = Field("", description="user id")
    location: Optional[str] = Field("", description="")
    time: Optional[str] = Field("", description="")
    appearance: Optional[str] = Field("", description="")
    symptoms: Optional[str] = Field("", description="")

class DBData(BaseModel):
    userid: Optional[str] = Field("", description="user id")

class InitializeData(BaseModel):
    userid: Optional[str] = Field("", description="user id")
    
class ChatData(BaseModel):
    userid: Optional[str] = Field("", description="user id")
    query: Optional[str] = Field("", description="")
