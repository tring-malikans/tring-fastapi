import motor.motor_asyncio
from bson import ObjectId
from decouple import config
# from binance.client import Client
# from binance.websockets import BinanceSocketManager
# import asyncio
# from binance import AsyncClient, BinanceSocketManager
from server.database.database_helper import student_helper, admin_helper ,order_helper

MONGO_DETAILS = "mongodb+srv://sufiyan:sufiyan@tring1.vef4g.mongodb.net/tringDatabase?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)


database = client.tring

student_collection = database.get_collection('students_collection')
admin_collection = database.get_collection('admins')
orders_collection = database.get_collection('tring-orders')
orders_logs_collection = database.get_collection('orders_logs')



# binance
# client = Client("FDNSdGoxcrJ9BlRiJOO5w1JbZCese78u61IkFMjVqRlbydY7Vk0bsqkJdgTQjt00", "d20M9XACmfIU0Dw3eH3qvhUwYHYvHxGnmgdPrpslyuD1pkRPoNTa85CqFFhZNUK4")
# bm = BinanceSocketManager(client)

async def add_admin(admin_data: dict) -> dict:
    admin = await admin_collection.insert_one(admin_data)
    new_admin = await admin_collection.find_one({"_id": admin.inserted_id})
    return admin_helper(new_admin)


async def retrieve_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students





async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True


async def update_student_data(id: str, data: dict):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        student_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True


# orders_logs

# async def retrieve_order_price():
#     def checkPrice(msg):
#         return msg
#     # def process_messageC(msg):
#     #     realtime_price=msg['p']
#     #     checkPrice(realtime_price)
#     # price=bm.start_aggtrade_socket('DOGEBUSD',process_messageC)
#     bm.start()
#     return checkPrice

async def retrieve_order_logs():
    order_logs = []
    async for order in orders_logs_collection.find():
        order_logs.append(order)
    # rec=await orders_logs_collection.find().sort([('_id', -1)]).limit(1)   .sort([('_id', -1)]).limit(1)
    # print(rec)
    return order_logs

async def retrieve_orders():
    orders = []
    async for order in orders_collection.find():
        orders.append(order_helper(order))
    return orders

async def add_order(order_data: dict) -> dict:
    order = await orders_collection.insert_one(order_data)
    new_order = await orders_collection.find_one({"_id": order.inserted_id})
    return order_helper(new_order)

async def update_order_data(id: str, data: dict):
    order = await orders_collection.find_one({"_id": ObjectId(id)})
    if order:
        orders_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True

async def delete_order(id: str):
    order = await orders_collection.find_one({"_id": ObjectId(id)})
    if order:
        await orders_collection.delete_one({"_id": ObjectId(id)})
        return True
