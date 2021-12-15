from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
from pymongo import MongoClient
import datetime
client = MongoClient('mongodb://localhost:27017')

db = client.personwork
collection = db['person']

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>person work</title>
    </head>
    <body>
        <h1>Введите имя работника</h1>
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

        if len(data) == 2:
            print('age-person')
            age = collection.find_one({'age': int(data)})
            await websocket.send_text(f"{age}")

        elif data.find("@") != data.find("@"):
            print("name")
            name = collection.find_one({'name': data})
            await websocket.send_text(f"{name}")

        elif data == datetime.datetime():
            print('data')
            company = collection.find_one({'join_date': data})
            await websocket.send_text(f"{company}")



        elif data == str(data):
            print('company')
            company = collection.find_one({'company': data})
            await websocket.send_text(f"{company}")



        else:
            print('Ты дебил')

if __name__ == '__main__':
    uvicorn.run(app)

