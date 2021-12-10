from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')


db = client.personwork


app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Задание</title>
    </head>
    <body>
        <h1>Сообщения</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Отправить</button>
        </form>
        <ol id='messages'>
        </ol>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
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


@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"{data}")
        bills_post = db.person.find_one({'name': data})
        await websocket.send_text(f"{bills_post}")
if __name__ == '__main__':
    uvicorn.run(app)