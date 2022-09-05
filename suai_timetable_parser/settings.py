import datetime
date = datetime.datetime.now().date()

USE_DB = True

mongo_connecting_string = 'mongodb://localhost:27017/'
mongo_db_name = 'SUAI_timetable'
mongo_collection_name = f'{date}'
# OR
json_path = 'example.json'
