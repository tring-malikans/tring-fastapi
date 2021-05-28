from fastapi import APIRouter,WebSocket, Body
from fastapi.encoders import jsonable_encoder
import json
from server.database.database import *
from server.models.student import *
from server.models.orders import *
import asyncio
from binance import AsyncClient, BinanceSocketManager
router = APIRouter()
# client = Client("FDNSdGoxcrJ9BlRiJOO5w1JbZCese78u61IkFMjVqRlbydY7Vk0bsqkJdgTQjt00", "d20M9XACmfIU0Dw3eH3qvhUwYHYvHxGnmgdPrpslyuD1pkRPoNTa85CqFFhZNUK4", {"verify": True, "timeout": 10000})
# bm = ThreadedWebsocketManager(api_key='FDNSdGoxcrJ9BlRiJOO5w1JbZCese78u61IkFMjVqRlbydY7Vk0bsqkJdgTQjt00', api_secret='d20M9XACmfIU0Dw3eH3qvhUwYHYvHxGnmgdPrpslyuD1pkRPoNTa85CqFFhZNUK4')
# bm.start()
@router.get("/", response_description="orders retrieved")
async def get_orders():
    orders = await retrieve_orders()
    return ResponseModel(orders, "orders data retrieved successfully") \
        if len(orders) > 0 \
        else ResponseModel(orders, "Empty list returned")

@router.websocket("/webprice")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    ts = bm.aggtrade_socket('DOGEBUSD')
    while True:
        async with ts as tscm:
            while True:
                res = await tscm.recv()
                await websocket.send_text(res['p'])
    # order_logs=await retrieve_order_price()
    # print(order_logs)
    # order_logs=json.dumps(order_logs, separators=(',', ':'),default=str)
    # print("dfgddfd")
    # while True:
        # data = await websocket.receive_text()
        # await websocket.send_json(order_logs)
        # def handle_socket_message(msg):
        #     print(f"message type: {msg['e']}")
        #     print(msg)

        # bm.start_kline_socket(callback=handle_socket_message, symbol='DOGEBUSD')
        # def process_messageC(msg):
        #     print(msg)
        #     realtime_price=msg['p']
        #     print(realtime_price)
        #     # await websocket.send_text(realtime_price)
        # bm.start_kline_socket(callback=process_messageC,symbol='DOGEBUSD')
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    order_logs=await retrieve_order_logs()
    # print(order_logs)
    # order_logs=json.dumps(order_logs, separators=(',', ':'),default=str)
    while True:
        # data = await websocket.receive_text()
        # await websocket.send_json(order_logs)
        await websocket.send_text("order_logs")

# @router.get("/{id}", response_description="Student data retrieved")
# async def get_student_data(id):
#     student = await retrieve_student(id)
#     return ResponseModel(student, "Student data retrieved successfully") \
#         if student \
#         else ErrorResponseModel("An error occured.", 404, "Student doesn'exist.")


@router.post("/create", response_description="Order data added into the database")
async def add_order_data(order: OrderModel = Body(...)):
    order = jsonable_encoder(order)
    new_order = await add_order(order)
    return ResponseModel(new_order, "Order added successfully.")


@router.delete("/{id}", response_description="Student data deleted from the database")
async def delete_order_data(id: str):
    deleted_order = await delete_order(id)
    return ResponseModel("Order with ID: {} removed".format(id), "Order deleted successfully") \
        if deleted_order \
        else ErrorResponseModel("An error occured", 404, "Order with id {0} doesn't exist".format(id))


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
