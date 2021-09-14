from mangum import Mangum
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# handler = Mangum(app=app)
def handler(event, context):
    if event.get("some-key"):
        # Do something or return, etc.
        return

    asgi_handler = Mangum(app)
    response = asgi_handler(event, context) # Call the instance with the event arguments

    return response