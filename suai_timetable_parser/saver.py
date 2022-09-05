import json

from mongo_client import RaspMongoClient


class Saver:
    @staticmethod
    def save_to_json(table: list | dict, table_path: str, indent: int = 2, ensure_ascii: bool = False):
        with open(table_path, 'w', encoding='utf8') as file:
            json.dump(table, file, indent=indent, ensure_ascii=ensure_ascii)

    @staticmethod
    def save_to_mongo(data: list | dict, bd: RaspMongoClient, collection: str):
        if isinstance(data, list):
            bd.insert_documents(data, collection)
        if isinstance(data, dict):
            bd.insert_document(data, collection)
