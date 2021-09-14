from pydantic import BaseModel, Field, EmailStr
from typing import Optional,List


class CoinModel(BaseModel):
    coin: str = Field(...)
    pair: str = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "coin": "coin",
                "pair": "BUSD"
            }
        }




def ResponseModel(data, message):
    return {
        "data": [
            data
        ],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
