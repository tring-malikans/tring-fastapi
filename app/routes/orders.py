from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import json
from app.database.database import *
from app.models.student import *
from app.models.orders import *
# from server.app import socket_manager as sm
import asyncio
from binance import AsyncClient, BinanceSocketManager
from binance.client import Client
import pymongo
from datetime import datetime
from typing import List
from starlette.websockets import WebSocket, WebSocketDisconnect
mongo1 =pymongo.MongoClient("mongodb+srv://tring:tring1@cluster0.vef4g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = mongo1['tring']
tring_logs = db.get_collection('orders_logs')
seconds_data=db.get_collection('seconds_data')
router = APIRouter()

# client = Client("FDNSdGoxcrJ9BlRiJOO5w1JbZCese78u61IkFMjVqRlbydY7Vk0bsqkJdgTQjt00", "d20M9XACmfIU0Dw3eH3qvhUwYHYvHxGnmgdPrpslyuD1pkRPoNTa85CqFFhZNUK4", {"verify": True, "timeout": 10000})
# bm = ThreadedWebsocketManager(api_key='FDNSdGoxcrJ9BlRiJOO5w1JbZCese78u61IkFMjVqRlbydY7Vk0bsqkJdgTQjt00', api_secret='d20M9XACmfIU0Dw3eH3qvhUwYHYvHxGnmgdPrpslyuD1pkRPoNTa85CqFFhZNUK4')
# bm.start()
class Notifier:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            await self._notify(message)

    async def push(self, msg: str):
        await self.generator.asend(msg)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def _notify(self, message: str):
        living_connections = []
        while len(self.connections) > 0:
            # Looping like this is necessary in case a disconnection is handled
            # during await websocket.send_text(message)
            websocket = self.connections.pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections = living_connections

notifier = Notifier()

# class SocketManager:
#     def __init__(self):
#         self.active_connections: List[(WebSocket, models.User)] = []

#     async def connect(self, websocket: WebSocket, user: models.User):
#         await websocket.accept()
#         self.active_connections.append((websocket, user))

#     async def get_online_users(self):
#         response = {"receivers": []}
#         for connection in self.active_connections:
#             response['receivers'].append(connection[1].username)

#         for connection in self.active_connections:
#             response.update({"sender": connection[1].username})
#             # this is causing the problem
#             await connection[0].send_json(response)

# notifier = SocketManager()

@router.get("/orders_logs", response_description="orders retrieved")
async def get_orders():
    orders = await retrieve_orders_logs()
    return ResponseModel(orders, "orders data retrieved successfully") \
        if len(orders) > 0 \
        else ResponseModel(orders, "Empty list returned")
@router.get("/get", response_description="orders retrieved")
async def get_orders():
    orders = await retrieve_orders()
    return ResponseModel(orders, "orders data retrieved successfully") \
        if len(orders) > 0 \
        else ResponseModel(orders, "Empty list returned")

@router.websocket("/binanceprice")
async def websocket_endpoint(binancePrice: WebSocket):
    await notifier.connect(binancePrice)
    # await binancePrice.accept()
    client = await AsyncClient.create()
    # while True:
    bm = BinanceSocketManager(client)
    ts = bm.aggtrade_socket('DOGEBUSD')
    try:
        async with ts as tscm:
            while True:
                res = await tscm.recv()
                order_data={"price":res['p']}
                order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
                await binancePrice.send_text(order_logs)
    except WebSocketDisconnect:
        notifier.remove(binancePrice)

# @sm.on('wsorder_logs')
# async def websocket_endpoint(pair:str,wsorderlog: WebSocket):
#     # await wsorderlog.accept()
#     # try:
#     while True:
#         order_logs=await retrieve_order_logs(pair)
#         await sm.emit(order_logs)
#         order_data={"order_logs":order_logs}
#         order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
#         await wsorderlog.send_text(order_logs)
#     except WebSocketDisconnect:
#         notifier.remove(wsorderlog)

@router.websocket("/wsorder_logs/{pair}")
async def websocket_endpoint(pair:str,wsorderlog: WebSocket):
    await notifier.connect(wsorderlog)
    
    # await wsorderlog.accept()
    pong= await wsorderlog.receive_text()
    try:
        while True:
            order_logs=await retrieve_order_logs(pair)
            order_data={"order_logs":order_logs}
            order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
            await wsorderlog.send_text(order_logs)
    except WebSocketDisconnect:
        notifier.remove(wsorderlog)


@router.websocket("/{coin}")
async def websocket_endpoint(coin:str,binancePrice: WebSocket):
    await notifier.connect(binancePrice)
    # await binancePrice.accept()
    client = await AsyncClient.create()
    # while True:
    bm = BinanceSocketManager(client)
    ts = bm.symbol_ticker_socket(coin) 
    try:
        async with ts as tscm:
            while True:
                # timeStamp = await binancePrice.receive_text()
                res = await tscm.recv()
                order_data={"price":res['c'],"change":res['P'],"volume":res['v'],"pair":coin}
                order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
                await binancePrice.send_text(order_logs)
                # await notifier._notify(order_logs)
    except WebSocketDisconnect:
        notifier.remove(binancePrice)


@router.websocket("/graphdata")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    try:
        while True:
            timeStamp = await websocket.receive_text()
            # orderfill_logs=await retrieve_orders_logss()
            order_logs1=await retrieve_orders_logs_websocket(timeStamp)
            order_data={"order_logs1":order_logs1}
            order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
            await websocket.send_text(order_logs)
    except WebSocketDisconnect:
        notifier.remove(websocket)
@router.websocket("/webprice")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client = await AsyncClient.create()
    # while True:
    bm = BinanceSocketManager(client)
    ts = bm.aggtrade_socket('DOGEBUSD')
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            order_logs=await retrieve_order_logs()
            timeStamp = await websocket.receive_text()
            # orderfill_logs=await retrieve_orders_logss()
            order_logs1=await retrieve_orders_logs_websocket(timeStamp)
            order_data={"order_logs":order_logs,"order_logs1":order_logs1,"price":res['p']}
            order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
            await websocket.send_text(order_logs)
    
@router.websocket("/order_logs")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # data = await websocket.receive_text()
        # await websocket.send_json(order_logs)
        await websocket.send_text(order_logs)
        # await websocket.send_text("order_logs")

@router.websocket("/seconds_data")
async def websocket_endpoint(websocket: WebSocket):
    values=[]
    newTime=None
    price=None
    count=0
    date1=None
    datas=None
    seconds1=None
    await websocket.accept()
    while True:
        for data in tring_logs.find():
            sec=[]
            for order in seconds_data.find().sort([('_id', -1)]).limit(1):
                sec.append(order)
            if len(sec)==0:
                s = data['date'] / 1000
                seconds=datetime.fromtimestamp(s).strftime('%S')
                # print(datas)
                if not newTime:
                    newTime=seconds
                    price=float(data['realtime_price'])
                    date1=data['date']
                    count=1
                    datas=data
                elif newTime==seconds:
                    count=count+1
                    price=price+float(data['realtime_price'])
                    # print('equal')
                else:
                    # print(count)
                    price=price/count
                    # print(price)
                    datas['realtime_price']=format(price,'.8f')
                    # datas['date']=date1
                    # print(datas,'data1')
                    del datas['_id']
                    # if 'lowest_price' in datas:
                    #     print(datas)
                    order_data={"seconds_data":datas}
                    order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
                    await websocket.send_text(order_logs)
                    seconds_data.insert_one(datas)
                    s1 = datas['date'] / 1000
                    seconds1=datetime.fromtimestamp(s1).strftime('%S')
                    # print(int(seconds)-int(seconds1))
                    diff=int(seconds)-int(seconds1)
                    if diff>1:
                        for i in range(1,diff):
                            del datas['_id']
                            s = datas['date']/1000 
                            d1=datetime.fromtimestamp(s)
                            unixtime = datetime.timestamp(d1)
                            s1 = unixtime+1
                            s1=str(s1)
                            s1=s1.replace('.','')
                            if len(s1)<14:
                                l1=len(s1)
                                l2=14-l1
                                s1=int(s1)
                                for i in range(1,l2):
                                    s1=s1*10
                                datas['date']=s1
                                seconds_data.insert_one(datas)
                                order_data={"seconds_data":datas}
                                order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
                                await websocket.send_text(order_logs)
                            else:
                                s1=int(s1)
                                datas['date']=s1
                                seconds_data.insert_one(datas)
                                order_data={"seconds_data":datas}
                                order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
                                await websocket.send_text(order_logs)
                    # else:
                    #     del datas['_id']
                    #     seconds_data.insert_one(datas)
                        # print(i)
                    # seconds_data.insert_one(datas)
                    # date1=data['date']
                    count=1
                    newTime=seconds
                    price=float(data['realtime_price'])
                    datas=data
            elif sec[0]['date'] < data['date']:
                s = data['date'] / 1000
                seconds=datetime.fromtimestamp(s).strftime('%S')
                # print(datas)
                if not newTime:
                    newTime=seconds
                    price=float(data['realtime_price'])
                    date1=data['date']
                    count=1
                    datas=data
                elif 'buy_price' in data or 'sell_price' in data: 
                    # print(count)
                    price=price/count
                    # print(price)
                    datas['realtime_price']=format(price,'.8f')
                    # datas['date']=date1
                    # print(datas,'data1')
                    del datas['_id']
                    # if 'lowest_price' in datas:
                    #     print(datas)
                    seconds_data.insert_one(datas)
                    order_data={"seconds_data":datas}
                    order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
                    print(order_logs,'lll')
                    await websocket.send_text(order_logs)
                    s1 = datas['date'] / 1000
                    seconds1=datetime.fromtimestamp(s1).strftime('%S')
                    # print(int(seconds)-int(seconds1))
                    diff=int(seconds)-int(seconds1)
                    # if diff>1:
                    #     for i in range(1,diff):
                    #         del datas['_id']
                    #         s = datas['date']/1000 
                    #         d1=datetime.fromtimestamp(s)
                    #         unixtime = datetime.timestamp(d1)
                    #         s1 = unixtime+1
                    #         s1=str(s1)
                    #         s1=s1.replace('.','')
                    #         if len(s1)<14:
                    #             l1=len(s1)
                    #             l2=14-l1
                    #             s1=int(s1)
                    #             for i in range(1,l2):
                    #                 s1=s1*10
                    #             datas['date']=s1
                    #             seconds_data.insert_one(datas)
                    #             order_data={"seconds_data":datas}
                    #             order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
                    #             await websocket.send_text(order_logs)
                    #         else:
                    #             s1=int(s1)
                    #             datas['date']=s1
                    #             seconds_data.insert_one(datas)
                    #             order_data={"seconds_data":datas}
                    #             order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
                    #             await websocket.send_text(order_logs)
                    # else:
                    #     del datas['_id']
                    #     seconds_data.insert_one(datas)
                        # print(i)
                    # seconds_data.insert_one(datas)
                    # date1=data['date']
                    count=1
                    newTime=seconds
                    price=float(data['realtime_price'])
                    datas=data
                elif newTime==seconds:
                    count=count+1
                    price=price+float(data['realtime_price'])
                    # print('equal')
                else:
                    # print(count)
                    price=price/count
                    # print(price)
                    datas['realtime_price']=format(price,'.8f')
                    # datas['date']=date1
                    # print(datas,'data1')
                    del datas['_id']
                    # if 'lowest_price' in datas:
                    #     print(datas)
                    seconds_data.insert_one(datas)
                    order_data={"seconds_data":datas}
                    order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
                    await websocket.send_text(order_logs)
                    s1 = datas['date'] / 1000
                    seconds1=datetime.fromtimestamp(s1).strftime('%S')
                    # print(int(seconds)-int(seconds1))
                    diff=int(seconds)-int(seconds1)
                    if diff>1:
                        for i in range(1,diff):
                            del datas['_id']
                            s = datas['date']/1000 
                            d1=datetime.fromtimestamp(s)
                            unixtime = datetime.timestamp(d1)
                            s1 = unixtime+1
                            s1=str(s1)
                            s1=s1.replace('.','')
                            if len(s1)<14:
                                l1=len(s1)
                                l2=14-l1
                                s1=int(s1)
                                for i in range(1,l2):
                                    s1=s1*10
                                datas['date']=s1
                                seconds_data.insert_one(datas)
                                order_data={"seconds_data":datas}
                                order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
                                await websocket.send_text(order_logs)
                            else:
                                s1=int(s1)
                                datas['date']=s1
                                seconds_data.insert_one(datas)
                                order_data={"seconds_data":datas}
                                order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
                                await websocket.send_text(order_logs)
                    # else:
                    #     del datas['_id']
                    #     seconds_data.insert_one(datas)
                        # print(i)
                    # seconds_data.insert_one(datas)
                    # date1=data['date']
                    count=1
                    newTime=seconds
                    price=float(data['realtime_price'])
                    datas=data


# PLace Market order
@router.post('/buy/{account}/{coin}/{pair}',response_description="PLace Buy Market Order")
async def place_buy_market_order(account:str,coin:str,pair:str):
    buy_order=await buy_market_order(account,coin,pair)
    return ResponseModel(buy_order, "placed buy order successfully.")
# PLace Market order
@router.post('/sell/{account}/{coin}/{pair}',response_description="PLace Buy sell Order")
async def place_sell_market_order(account:str,coin:str,pair:str):
    sell_order=await sell_market_order(account,coin,pair)
    return ResponseModel(sell_order, "placed Sell order successfully.")
# meet threshold  order
@router.post('/thresholdmeet/{id}',response_description="Threshold meet")
async def threshold_meet_order(id:str):
    buy_order=await sell_threshold_meet(id)
    return ResponseModel(buy_order, "Threshold meet order successfully.")

@router.get("/getBalance", response_description="Get Binance Pair Balance")
async def add_order_data():
    client = Client("FDNSdGoxcrJ9BlRiJOO5w1JbZCese78u61IkFMjVqRlbydY7Vk0bsqkJdgTQjt00", "d20M9XACmfIU0Dw3eH3qvhUwYHYvHxGnmgdPrpslyuD1pkRPoNTa85CqFFhZNUK4")
    balance = client.get_asset_balance(asset='BUSD')
    return balance
@router.post("/create", response_description="Order data added into the database")
async def add_order_data(order: OrderModel = Body(...)):
    order = jsonable_encoder(order)
    new_order = await add_order(order)
    return ResponseModel(new_order, "Order added successfully.")

@router.get("/datas",response_description="Get Datas")
async def get_datas():
    orders = await retrieve_datas()
    return ResponseModel(orders, "orders data retrieved successfully") \
        if len(orders) > 0 \
        else ResponseModel(orders, "Empty list returned")
# @router.delete("/{id}", response_description="Student data deleted from the database")
# async def delete_order_data(id: str):
#     deleted_order = await delete_order(id)
#     return ResponseModel("Order with ID: {} removed".format(id), "Order deleted successfully") \
#         if deleted_order \
#         else ErrorResponseModel("An error occured", 404, "Order with id {0} doesn't exist".format(id))


@router.put("/{id}")
async def update_order(id: str, req: UpdateOrderModel = Body(...)):
    updated_order = await update_order_data(id, req.dict())
    orders = await retrieve_orders()
    return ResponseModel(orders, "orders data retrieved successfully") \
        if len(orders) > 0 \
        else ResponseModel(orders, "Empty list returned")
    # return ResponseModel("order with ID: {} status update is successful".format(id),
    #                      "order status updated successfully") \
    #     if updated_order \
    #     else ErrorResponseModel("An error occurred", 404, "There was an error updating the order.".format(id))
