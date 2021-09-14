from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import json
from database.database import *
from models.student import *
from models.orders import *
# from server.app import socket_manager as sm
# import asyncio
from binance import AsyncClient, BinanceSocketManager
from binance.client import Client
import pymongo
from datetime import datetime
from typing import List
from starlette.websockets import WebSocket, WebSocketDisconnect
mongo1=pymongo.MongoClient('mongodb+srv://sufiyan:sufiyan@tring1.vef4g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = mongo1['tring']
tring_logs = db.get_collection('orders_logs')
seconds_data=db.get_collection('seconds_data')
router = APIRouter()