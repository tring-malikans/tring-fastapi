from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UsersModel(BaseModel):
    accountname: str = Field(...)
    email: EmailStr = Field(...)
    coin: str = Field(...)
    pair: str = Field(...)
    api_key: str = Field(...)
    secret_key: str = Field(...)
    price: str = Field(...)
    status: bool = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "accountname": "name",
                "email": "name@gmail.com",
                "coin": "doge",
                "pair": "busd",
                "price": "100",
                "api_key": "api key",
                "secret_key": "secret key",
                "status": True,
            }
        }


class UpdateUsersModel(BaseModel):
    accountname: Optional[str]
    email: Optional[EmailStr]
    coin: Optional[str]
    pair: Optional[str]
    apikey: Optional[str]
    secret_key: Optional[str]
    price: Optional[str]
    status: Optional[bool]
    class Config:
        schema_extra = {
            "example": {
                "accountname": "name",
                "email": "name@gmail.com",
                "coin": "doge",
                "pair": "busd",
                "price": "100",
                "api_key": "api key",
                "secret_key": "secret key",
                "status": True,
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
