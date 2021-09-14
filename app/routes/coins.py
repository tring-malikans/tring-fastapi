from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import json
from database.database import *
from models.coins import *
# import asyncio
from binance import AsyncClient, BinanceSocketManager
from binance.client import Client
import pymongo
from datetime import datetime
from typing import List
from starlette.websockets import WebSocket, WebSocketDisconnect
router = APIRouter()


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
                res = await tscm.recv()
                order_data={"price":res['c'],"change":res['P'],"volume":res['v'],"pair":coin}
                order_logs=json.dumps(order_data, separators=(',', ':'),default=str)
                await binancePrice.send_text(order_logs)
    except WebSocketDisconnect:
        notifier.remove(binancePrice)



@router.get("/getcoins", response_description="Get Coins")
async def add_order_data():
    coins=await retrieve_coins()
    return coins


@router.post("/createcoin", response_description="Create Coins")
async def add_coin_data(coin: CoinModel = Body(...)):
    coin = jsonable_encoder(coin)
    new_coin = await add_coin(coin)
    return ResponseModel(new_coin, "Order added successfully.")
        