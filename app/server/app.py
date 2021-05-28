from fastapi import FastAPI, WebSocket, Depends
from fastapi.responses import HTMLResponse
from .auth.jwt_bearer import JWTBearer
from .routes.student import router as StudentRouter
from .routes.orders import router as OrderRouter
from .routes.admin import router as AdminRouter
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "https://localhost.9000",
    "http://localhost",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
# async def read_root():
#     return {"message": "Welcome to this fantastic app, sighs."}



app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
# app.include_router(StudentRouter, tags=["Students"], prefix="/student", dependencies=[Depends(token_listener)])
# app.include_router(StudentRouter, tags=["Students"], prefix="/student")
app.include_router(OrderRouter, tags=["Orders"], prefix="/orders")
