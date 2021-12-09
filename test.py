import requests

try:
    from pymongo import MongoClient
except ImportError:
    raise ImportError('PyMongo is not installed')


class MongoDB(object):
    def __init__(self, host='localhost', port=27017, database_name=None, collection_name=None):
        try:
            self._connection = MongoClient(host=host, port=port, maxPoolSize=200)
        except Exception as error:
            raise Exception(error)
        self._database = None
        self._collection = None
        if database_name:
            self._database = self._connection[database_name]
        if collection_name:
            self._collection = self._database[collection_name]

    def insert(self, post):
        # add/append/new single record
        post_id = self._collection.insert_one(post).inserted_id
        return post_id


url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/CAN.csv'
response = requests.get(url)
data = response.text
if response.status_code != 200:
    print('Failed to get data:', response.status_code)
else:
    print('First 100 characters of data are')
    print(data[:100])

print('[*] Parsing response text')
data = data.split('\n')
data_list = list()
for value in data:
    if 'year,data' not in value:
        if value:
            value = value.split(',')
            data_list.append({'year': int(value[0]), 'data': float(value[1])})

print(data_list)

print('[*] Pushing data to MongoDB ')
mongo_db = MongoDB(database_name='Climate_DB', collection_name='climate_data')

for collection in data_list:
    print('[!] Inserting - ', collection)
    mongo_db.insert(collection)