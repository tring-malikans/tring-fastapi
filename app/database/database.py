# import motor.motor_asyncio
from bson import ObjectId
from decouple import config
from binance.client import Client
import datetime
# from binance.websockets import BinanceSocketManager
# import asyncio
# from binance import AsyncClient, BinanceSocketManager
from database.database_helper import student_helper, admin_helper ,order_helper, coin_helper ,user_helper
import pymongo
MONGO_DETAILS = "mongodb+srv://tring:tring@tring1.vef4g.mongodb.net/tringDatabase?retryWrites=true&w=majority"

# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
client =pymongo.MongoClient("mongodb+srv://tring:tring1@cluster0.vef4g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


database = client.tring
database1 = client.price_history

datas_collection=database1.get_collection('DOGEBUSDAggr')

admin_collection = database.get_collection('admins')
orders_collection = database.get_collection('orders')
coins_collection = database.get_collection('coins_list')

orders_logs_collection = database.get_collection('orders_logs')
ordersfill_logs_collection = database.get_collection('ordersfill')
seconds_logs_collection = database.get_collection('seconds_data')
student_collection = database.get_collection('students_collection')
user_collection = database.get_collection('users')



# binance
binace_client = Client("FDNSdGoxcrJ9BlRiJOO5w1JbZCese78u61IkFMjVqRlbydY7Vk0bsqkJdgTQjt00", "d20M9XACmfIU0Dw3eH3qvhUwYHYvHxGnmgdPrpslyuD1pkRPoNTa85CqFFhZNUK4")
# bm = BinanceSocketManager(client)

async def retrieve_datas():
    orders = []
    async for order in datas_collection.find():
        order['_id']=str(order['_id'])
        orders.append(order)
    return orders

async def add_admin(admin_data: dict) -> dict:
    admin = admin_collection.insert_one(admin_data)
    new_admin = admin_collection.find_one({"_id": admin.inserted_id})
    return admin_helper(new_admin)

async def retrieve_user(id: str) -> dict:
    user = await admin_collection.find_one({"_id": ObjectId(id)})
    if user:
        return admin_helper(user)
        
async def update_fav_coin_user(id: str, data: dict):
    fav_coin = await admin_collection.find_one({"_id": ObjectId(id)})
    if fav_coin:
        admin_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True

async def retrieve_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students


# Users
# Get All
async def retrieve_users():
    users = []
    for user in user_collection.find():
        users.append(user_helper(user))
    return users
# Get ONe
async def retrieve_user1(_id: str) -> dict:
    user = user_collection.find_one({"_id": ObjectId(_id)})
    if user:
        return user_helper(user)
# Get ONe
async def retrieve_user(id: str) -> dict:
    user = user_collection.find_one({"accountname": id})
    if user:
        return user_helper(user)
# Add user
async def add_user(user_data: dict) -> dict:
    findUser = user_collection.find_one({"accountname": user_data['accountname']})
    if isinstance(findUser,dict):
        return {
            "error":"Already Exists User Name"
        }
    else:
        user = user_collection.insert_one(user_data)
        new_user =  user_collection.find_one({"_id": user.inserted_id})
        return user_helper(new_user)
# Update
async def update_user_data(id: str, data: dict):
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        user_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True
# Delete
async def delete_user(id: str):
    
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        user_collection.delete_one({"_id": ObjectId(id)})
        return True



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
async def retrieve_orders_logs():
    orders = []
    async for order in seconds_logs_collection.find():
    # async for order in ordersfill_logs_collection.find():
    # async for order in orders_logs_collection.find():
        order["_id"]=str(order["_id"])
        orders.append(order)
    # print(orders)
    return orders
async def retrieve_orders_logss():
    orders = []
    async for order in ordersfill_logs_collection.find():
    # async for order in orders_logs_collection.find():
        order["_id"]=str(order["_id"])
        orders.append(order)
    # print(orders)
    return orders
async def retrieve_orders_logs_websocket(timeStamp):
    orders = []
    timeStamp=int(timeStamp)
    print(timeStamp)
    async for order in seconds_logs_collection.find():
    # async for order in orders_logs_collection.find():
        if timeStamp:
            if order['date'] > timeStamp:
                order["_id"]=str(order["_id"])
                orders.append(order)
    # print(orders)
    return orders
async def retrieve_order_logs(pair):
    order_logs = []
    # async for order in orders_collection.find().sort([('_id', -1)]).limit(1):
    async for order in orders_collection.find():
        if str(order['_id'])==pair:
            # if not order['trade_status']:
            order_logs.append(order)
            #     if order['pair']==pair:
    # rec=await orders_logs_collection.find().sort([('_id', -1)]).limit(1)   .sort([('_id', -1)]).limit(1)
    # rec=await orders_logs_collection.find().sort([('_id', -1)]).limit(1)
    # print(rec)
    if len(order_logs)>=1:
        return order_logs[0]
    else:
        return []

# Calculate threshold_price
def updateThresholdPriceValue(buy_price,threshold_percentage):
    threshold_value=buy_price*threshold_percentage/100
    threshold_price=buy_price+threshold_value
    threshold_price=format(threshold_price,'.5f')
    threshold_price=float(threshold_price)
    return {
        "threshold_price":threshold_price,
    }
# Calculate loss_sell_price  
def updateLossSellPriceValue(buy_price,loss_sell_percentage):
    loss_sell_value=buy_price*loss_sell_percentage/100
    loss_sell_price=buy_price-loss_sell_value
    loss_sell_price=format(loss_sell_price,'.5f')
    loss_sell_price=float(loss_sell_price)
    return {
        "loss_sell_price":loss_sell_price,
    }
async def buy_market_order(account:str,coin:str,pair:str):
    # async for order in orders_collection.find():
    #     if str(order['_id'])==id:
            # quantity=order['amount_quantity']
            # if order['buy_quantity']:
    user = user_collection.find_one({"accountname": account})
    if user['status']:
        # binance
        binace_client = Client(user['api_key'], user['secret_key'])
        # value=binace_client.get_asset_balance(asset=pair.upper())
        # quantity=value['free']
        quantity=float(user['price'])
        pairname=coin.upper()+pair.upper()
        orderBuy = binace_client.order_market_buy(symbol=pairname,quoteOrderQty=quantity)
        # Calculate duration between buy order placed and confirmation recieved on exchange 
        buy_order_time = datetime.datetime.now()
        # Binance Order Time format conversion 
        unixtimestamp = orderBuy['transactTime'] / 1000
        binance_buy_order_time_unix = datetime.datetime.fromtimestamp(unixtimestamp)
        binance_buy_order_time=datetime.datetime.fromtimestamp(unixtimestamp).strftime(f'%m-%d %H:%M:%S,%f')[:-3]
        time1=f"{binance_buy_order_time_unix:%m-%d-%Y %H:%M:%S:%MS}"
        # get duration
        difference = buy_order_time - binance_buy_order_time_unix
        # get seconds 
        seconds=difference.seconds
        # get milli seconds
        micro=int(str(difference.microseconds)[:3])
        # combine both "ss ms"
        micros=f'{seconds} {micro}'
        print(orderBuy,'buy')
        # updateAutoScalp=None
        # updateAutoScalp['buy_order_filled']=True
        # updateAutoScalp['buy_quantity']=orderBuy['executedQty']
        # if not updateAutoScalp['first_quantity']:
        #     updateAutoScalp['first_quantity']=orderBuy['executedQty']
        # updateAutoScalp["buy_price"]=float(orderBuy['fills'][0]['price'])
        # updateAutoScalp["binance_buy_order_time"]=binance_buy_order_time
        # updateAutoScalp['amount_quantity']=quantity
        # updateAutoScalp['buy_order']=orderBuy
        # # Insert highest_price 
        # updateAutoScalp['highest_price']=float(orderBuy['fills'][0]['price'])

        # # Insert loss_sell_price
        # getValues=updateLossSellPriceValue(float(orderBuy['fills'][0]['price']),order['loss_sell_percentage'])
        # updateAutoScalp['loss_sell_price']=getValues['loss_sell_price']
        
        # # Insert threshold_price
        # getValues=updateThresholdPriceValue(float(orderBuy['fills'][0]['price']),order['threshold_percentage'])
        # updateAutoScalp['threshold_price']=getValues['threshold_price']
        # update Buy order
        order = orders_collection.insert_one(orderBuy)
        user['quan']=orderBuy['executedQty']
        user_collection.update_one({"_id": ObjectId(user['_id'])}, {"$set": user})
        return {
            "name":coin+'/'+pair,
            "time":time1
        }
    else:
        return {
            "error":"User not Found or status is false"
        }
    # orders_collection.update_one({"_id": ObjectId(id),}, {"$set": updateAutoScalp})

# Calculate target_buy_price
def updateTargetBuyPriceValue(lowest_price,up_percentage):
    up_value=lowest_price*up_percentage/100
    target_buy_price=lowest_price+up_value
    target_buy_price=format(target_buy_price,'.5f')
    target_buy_price=float(target_buy_price)
    return {
        "target_buy_price":target_buy_price,
    }
# Sell market order
async def sell_market_order(account:str,coin:str,pair:str):
    user = user_collection.find_one({"accountname": account})
    if user['status']:
        # binance
        binace_client = Client(user['api_key'], user['secret_key'])
        # value=binace_client.get_asset_balance(asset=coin.upper())
        # quantity=value['free']
        # # quantity=float(quantity)-0.5
        quantity=float(user['quan'])

        quantity=format(quantity,'.1f')
        pairname=coin.upper()+pair.upper()
        print(quantity)
        # Place sell order
        orderSell = binace_client.order_market_sell(symbol=pairname,quantity=quantity)
        # Calculate duration between sell order placed and confirmation recieved on exchange 
        sell_order_time = datetime.datetime.now()

        # Binance Order Time format conversion 
        unixtimestamp = orderSell['transactTime'] / 1000
        binance_sell_order_time_unix = datetime.datetime.fromtimestamp(unixtimestamp)
        print(binance_sell_order_time_unix)
        print(f"{binance_sell_order_time_unix:%m-%d-%Y %H:%M:%S:%MS}")
        time1=f"{binance_sell_order_time_unix:%m-%d-%Y %H:%M:%S:%MS}"
        print(orderSell)
        # Get duration
        difference = sell_order_time - binance_sell_order_time_unix

        # Get seconds
        seconds=difference.seconds

        # Get milli seconds
        micro=int(str(difference.microseconds)[:3])
        # combine both "ss ms"
        micros=f'{seconds} {micro}'
        # updateAutoScalp=order
        # updateAutoScalp['buy_order_filled']=False
        # updateAutoScalp['buy_quantity']=orderSell['executedQty']
        # updateAutoScalp['last_quantity']=orderSell['executedQty']
        # updateAutoScalp['last_amount']=float(orderSell['executedQty'])*float(orderSell['fills'][0]['price'])
        # updateAutoScalp["profit_loss"]="profit"
        # updateAutoScalp["buy_price"]=0
        # updateAutoScalp['threshold_status']=False
        # updateAutoScalp['target_sell_price']=0
        # lowest_price=float(orderSell['fills'][0]['price'])
        # updateAutoScalp['lowest_price']=lowest_price
        # getValues=updateTargetBuyPriceValue(lowest_price,order['up_percentage'])
        # updateAutoScalp['target_buy_price']=getValues['target_buy_price']
        # update tring_orders
        orders_collection.insert_one(orderSell)
        user['price']=str(float(orderSell['cummulativeQuoteQty']))
        user_collection.update_one({"_id": ObjectId(user['_id'])}, {"$set": user})
        return {
            "name":coin+'/'+pair,
            "time":time1
        }
    else:
        return {
            "error":"User not Found or status is false"
        }

# calculate target_sell_price
def calculateTargetSellPriceValue(highest_price,down_percentage):
    down_value=highest_price*down_percentage/100
    target_sell_price=highest_price-down_value
    target_sell_price=format(target_sell_price,'.5f')
    target_sell_price=float(target_sell_price)
    return {
        "target_sell_price":target_sell_price
    }
# Threshold meet order
async def sell_threshold_meet(id:str):
    async for order in orders_collection.find():
        if str(order['_id'])==id:
            getValues=calculateTargetSellPriceValue(order['highest_price'],order['down_percentage'])
            # Update target_sell_price
            # Update threshold_status
            updateAutoScalp=order
            updateAutoScalp['threshold_status']=True
            updateAutoScalp['threshold_price']=order['highest_price']
            updateAutoScalp['target_sell_price']=getValues['target_sell_price']
            orders_collection.update_one({"_id": ObjectId(id),}, {"$set": updateAutoScalp})
async def retrieve_orders():
    orders = []
    async for order in orders_collection.find():
        if not order['trade_status']:
            orders.append(order_helper(order))
    return orders

async def add_order(order_data: dict) -> dict:
    order = await orders_collection.insert_one(order_data)
    new_order = await orders_collection.find_one({"_id": order.inserted_id})
    return order_helper(new_order)
    # return new_order

async def update_order_data(id: str, data: dict):
    order = await orders_collection.find_one({"_id": ObjectId(id)})
    if order:
        orders_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True

# async def delete_order(id: str):
#     order = await orders_collection.find_one({"_id": ObjectId(id)})
#     if order:
#         await orders_collection.delete_one({"_id": ObjectId(id)})
#         return True


# Coins_list
async def retrieve_coins():
    coins = []
    async for coin in coins_collection.find():
        coins.append(coin_helper(coin))
    return coins

async def add_coin(coin_data: dict) -> dict:
    coin = await coins_collection.insert_one(coin_data)
    new_coin = await coins_collection.find_one({"_id": coin.inserted_id})
    return coin_helper(new_coin)



