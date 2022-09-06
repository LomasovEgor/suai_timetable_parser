import os

USE_DB = True

mongo_connecting_string = os.environ['MONGODB']
mongo_db_name = os.environ['MONGODB_NAME']
mongo_collection_name = f'lessons'
# OR
json_path = 'example.json'
