from pydantic import BaseModel, Field, EmailStr
from typing import Optional,List


class Accounts(BaseModel):
    exchange: str = Field(...)
    account_type: str = Field(...)
    main_account: str = Field(...)
    account_name: str = Field(...)
    account_email: str = Field(...)
    key: str = Field(...)
    secret_key: str = Field(...)

class favCoin(BaseModel):
    coin:str=Field(...)
class AdminModel(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    # fav_coins:List[favCoin]=Field(...)
    # accounts: List[Accounts] = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "fullname": "Admin",
                "email": "admin@gmail.com",
                "password": "admin"
            }
        }
class UpdateAdminModel(BaseModel):
    fav_coins:List[str]=[]
    # fav_coins:str=Field(...)
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "fullname": "Admin",
    #             "email": "admin@gmail.com",
    #             "password": "admin"
    #         }
    #     }


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
