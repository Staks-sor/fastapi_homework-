from pymongo import MongoClient
from fastapi import FastAPI
import os
from typing import Optional
import uvicorn

var_mongopass = os.getenv('staks')
var_url='mongodb+srv://staks:stas1234@cluster0.tutwf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

app = FastAPI()

client = MongoClient(var_url)

mydb = client['person']
mycol = mydb['personwork']

@app.get('/')
async def read_root():
    return {"Hello World"}



if __name__ == '__main__':
    uvicorn.run(app)