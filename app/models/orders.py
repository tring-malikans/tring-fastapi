from typing import Optional,List

from pydantic import BaseModel,  Field

    
# class OrderModel(BaseModel):
#     # exchange: str = Field(...)
#     # account_name: str = Field(...)
#     # account_type: str = Field(...)
#     # main_account: str = Field(...)
#     # account_balance: str = Field(...)
#     # limit_price: float = None
#     # stop_loss_price: float = None
#     pair: str = Field(...)
#     trade_type: str = Field(...)
#     auto_scalp:Optional[AutoScalp] = None
#     amount_quantity:Optional[AmountQuantity]=None
#     class Config:
#         schema_extra = {
#             "example": {
#                 "pair": "DOGEBUSD",
#                 "exchange": "Binance",
#                 "account_name": "",
#                 "account_type": "",
#                 "main_account": "",
#                 "account_balance": "",
#                 "trade_type": "limit",
#                 "auto_scalp":{},
#                 "limit_price":"",
#                 "stop_loss_price":"",
#             }
#         }
class BuyOrder(BaseModel): 
    lowest_price: float=None
    target_buy_price : float=None
    order_place_at:str=None
    entry_time:str=None
    in_amount:str=None
    in_amount_pair:str=None
    quantity:str=None
    # in_quantity:str=None
    # in_quantity_pair:str=None
    entry_price:str=None
    entry_price_pair:str=None
    fees_amount:str=None
    fees_amount_pair:str=None
    fees_percentage:str=None
    buy_order_status:bool=None
    order_status_code:str=None
class SellOrder(BaseModel): 
    highest_price: float=None
    target_sell_price : float=None
    loss_sell_price : float=None
    threshold_price : float=None
    order_place_at:str=None
    entry_time:str=None
    in_amount:str=None
    in_amount_pair:str=None
    in_quantity:str=None
    in_quantity_pair:str=None
    entry_price:str=None
    entry_price_pair:str=None
    fees_amount:str=None
    fees_amount_pair:str=None
    fees_percentage:str=None
    buy_order_status:bool=None
    order_status_code:str=None
class Runs(BaseModel):
    run_no: str= None
    entry_time: str =None
    exit_time: str =None
    duration: str =None
    in_amount: str =None
    in_amount_pair: str =None
    in_quantity: str =None
    in_quantity_pair: str =None
    out_amount: str =None
    out_amount_pair: str =None
    out_quantity: str =None
    out_quantity_pair: str =None
    entry_price: str =None
    entry_price_pair: str =None
    exit_price: str =None
    exit_price_pair: str =None
    fees_amount: str =None
    fees_amount_pair: str =None
    fees_percentage: str =None
    profit_loss: str =None
    profit_loss_amount: str =None
    profit_loss_pair: str =None
    profit_loss_percentage: str =None
    run_status: str =None
    buy_order:BuyOrder=None
    sell_order:SellOrder=None
class OrderModel(BaseModel):
    coin: str =Field(...)
    pair: str =Field(...)
    exchange: str =Field(...)
    trade_type: str =Field(...)
    account_balance: str =Field(...)
    main_account: str =Field(...)
    account_type: str =Field(...)
    account_name: str =Field(...)
    up_percentage: float =None
    down_percentage: float =None
    loss_sell_percentage: float =None
    threshold_percentage: float =None
    buy_quantity: str =None
    amount_quantity: str =None
    first_amount: str =None
    first_quantity: str =None
    # entry_time: str =None
    # exit_time: str =None
    # duration: str =None
    # in_amount: str =None
    # in_amount_pair: str =None
    # in_quantity: str =None
    # in_quantity_pair: str =None
    # out_amount: str =None
    # out_amount_pair: str =None
    # out_quantity: str =None
    # out_quantity_pair: str =None
    # entry_price: str =None
    # entry_price_pair: str =None
    # exit_price: str =None
    # exit_price_pair: str =None
    # fees_amount: str =None
    # fees_amount_pair: str =None
    # fees_percentage: str =None
    # profit_loss: str =None
    # profit_loss_amount: str =None
    # profit_loss_pair: str =None
    # profit_loss_percentage: str =None
    # runs:List[Runs]=None
    # for backend script
    auto_trail:bool=None
    trade_status: bool =None
    lowest_price: float=None
    target_buy_price: float =None
    highest_price: float=None
    target_sell_price: float =None
    loss_sell_price: float =None
    threshold_price: float =None
    threshold_status: bool=False
    buy_price: float =None
    buy_order_filled: bool =False


class UpdateOrderModel(BaseModel):
    coin: str =Field(...)
    pair: str =Field(...)
    exchange: str =Field(...)
    trade_type: str =Field(...)
    account_balance: str =Field(...)
    main_account: str =Field(...)
    account_type: str =Field(...)
    account_name: str =Field(...)
    up_percentage: float =None
    down_percentage: float =None
    loss_sell_percentage: float =None
    threshold_percentage: float =None
    buy_quantity: str =None
    amount_quantity: str =None
    # entry_time: str =None
    # exit_time: str =None
    # duration: str =None
    # in_amount: str =None
    # in_amount_pair: str =None
    # in_quantity: str =None
    # in_quantity_pair: str =None
    # out_amount: str =None
    # out_amount_pair: str =None
    # out_quantity: str =None
    # out_quantity_pair: str =None
    # entry_price: str =None
    # entry_price_pair: str =None
    # exit_price: str =None
    # exit_price_pair: str =None
    # fees_amount: str =None
    # fees_amount_pair: str =None
    # fees_percentage: str =None
    # profit_loss: str =None
    # profit_loss_amount: str =None
    # profit_loss_pair: str =None
    # profit_loss_percentage: str =None
    # runs:List[Runs]=None
    trade_status: bool =None
    threshold_status: bool=False
    # for backend script
    lowest_price: float=None
    target_buy_price: float =None
    highest_price: float=None
    target_sell_price: float =None
    loss_sell_price: float =None
    threshold_price: float =None
    buy_price: float =None
    buy_order_filled: bool =False

# class UpdateOrderModel(BaseModel):
#     pair: str = Field(...)
#     # exchange: str = Field(...)
#     # account_name: str = Field(...)
#     # account_type: str = Field(...)
#     # main_account: str = Field(...)
#     # account_balance: str = Field(...)
#     trade_type: str = Field(...)
#     auto_scalp:Optional[AutoScalp] = None
#     amount_quantity:Optional[AmountQuantity]=None
#     limit_price: float = None
#     stop_loss_price: float = None
#     class Config:
#         schema_extra = {
#             "example": {
#                 "pair": "DOGEBUSD",
#                 "exchange": "Binance",
#                 "account_name": "",
#                 "account_type": "",
#                 "main_account": "",
#                 "account_balance": "",
#                 "trade_type": "limit",
#                 "auto_scalp":{},
#                 "limit_price":"",
#                 "stop_loss_price":"",
#             }
#         }



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
