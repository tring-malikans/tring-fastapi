# import socketio
from fastapi import FastAPI, WebSocket, Depends
from fastapi.responses import HTMLResponse
from .auth.jwt_bearer import JWTBearer
# from .routes.student import router as StudentRouter
from .routes.users import router as UserRouter
from .routes.orders import router as OrderRouter
from .routes.admin import router as AdminRouter
from .routes.coins import router as CoinRouter
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from mangum import Mangum
import uvicorn
import os
# from fastapi_socketio import SocketManager
app = FastAPI()

port = os.environ["PORT"]
# origins = [
#     "https://localhost.9000",
#     "http://localhost",
#     "http://localhost:8000",
# ]

middleware = [ Middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['*'],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app = FastAPI(middleware=middleware)
# sio = socketio.AsyncServer(async_mode='asgi')    
# socket_app = socketio.ASGIApp(sio,socketio_path="socket.io")    
background_task_started = False    
# sio = SocketManager(app=app)
# @sio.on('wsorder_logs')
# async def handle_join(sid, *args, **kwargs):
#     await sio.emit('lobby', 'User joined')

# @sio.on("message")
# async def handle_message(sid, data: str):
#     print("message:", data)
#     # Broadcast the received message to all connected clients.
#     # See: https://python-socketio.readthedocs.io/en/latest/server.html#emitting-events
#     await sio.emit("response", data)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            # var ws = new WebSocket("ws://localhost:9000/orders/ws");
            ws.onmessage = function(event) {
                console.log(event.data)
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
token_listener = JWTBearer()

@app.get("/", tags=["Root"])
async def get():
    return HTMLResponse(html)
async def read_root():
    return {"message": "Welcome to this fantastic app, sighs."}



app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
# app.include_router(StudentRouter, tags=["Students"], prefix="/student", dependencies=[Depends(token_listener)])
# app.include_router(StudentRouter, tags=["Students"], prefix="/student")
app.include_router(OrderRouter, tags=["Orders"], prefix="/api")
app.include_router(CoinRouter, tags=["Coins"], prefix="/coins")
app.include_router(UserRouter, tags=["Users"], prefix="/users")
# app.mount('/soc', socket_app)
handler = Mangum(app=app)


# Assalamualikum Hamad bhai
# bhai any resources have on Fastapi socket io?



if __name__ == '__main__':
    uvicorn.run('server.app:app', host="0.0.0.0", port=port, reload=True)