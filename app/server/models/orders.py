from typing import Optional,List

from pydantic import BaseModel,  Field

class Runs(BaseModel):
    realtime_price: float = None
    lowest_price: float = None
    target_buy_price: float = None
    highest_price: float = None
    loss_sell_price: float = None
    threshold_price: float = None
    threshold_status: bool = None
    target_sell_price: float = None
    buy:dict=None
    sell:dict=None
    profit_loss:str=None

class AutoScalp(BaseModel):
    # entry_type: str = None
    buy_quantity:float=None
    up_percentage: float = None
    down_percentage: float = None
    threshold_percentage: float = None
    loss_sell_percentage: float = None
    runs:Optional[List[Runs]]=None
    
    buy_order_filled:Optional[bool]=False
    lowest_price: Optional[float] = None
    target_buy_price: Optional[float] = None
    highest_price: Optional[float] = None
    loss_sell_price: Optional[float] = None
    threshold_price: Optional[float] = None
    threshold_status: Optional[bool] = None
    target_sell_price: Optional[float] = None

class AmountQuna(BaseModel):
    amount: Optional[float]=None
    quantity: Optional[float]=None
    percent: Optional[float]=None
    
class OrderModel(BaseModel):
    pair: str = Field(...)
    # exchange: str = Field(...)
    # account_name: str = Field(...)
    # account_type: str = Field(...)
    # main_account: str = Field(...)
    # account_balance: str = Field(...)
    trade_type: str = Field(...)
    auto_scalp:Optional[AutoScalp] = None
    amount_quantity:Optional[AmountQuna]=None
    limit_price: float = None
    stop_loss_price: float = None
    class Config:
        schema_extra = {
            "example": {
                "pair": "DOGEBUSD",
                "exchange": "Binance",
                "account_name": "",
                "account_type": "",
                "main_account": "",
                "account_balance": "",
                "trade_type": "limit",
                "auto_scalp":{},
                "limit_price":"",
                "stop_loss_price":"",
            }
        }


class UpdateOrderModel(BaseModel):
    pair: str = Field(...)
    # exchange: str = Field(...)
    # account_name: str = Field(...)
    # account_type: str = Field(...)
    # main_account: str = Field(...)
    # account_balance: str = Field(...)
    trade_type: str = Field(...)
    auto_scalp:Optional[AutoScalp] = None
    amount_quantity:Optional[AmountQuna]=None
    limit_price: float = None
    stop_loss_price: float = None
    class Config:
        schema_extra = {
            "example": {
                "pair": "DOGEBUSD",
                "exchange": "Binance",
                "account_name": "",
                "account_type": "",
                "main_account": "",
                "account_balance": "",
                "trade_type": "limit",
                "auto_scalp":{},
                "limit_price":"",
                "stop_loss_price":"",
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
