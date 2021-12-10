from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')


db = client.personwork
bills_post = db.person.find_one({'name': 'Flynn Vang'})
print(bills_post)