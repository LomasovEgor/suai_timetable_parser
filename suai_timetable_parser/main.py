import loguru

from group_id_parser import GroupIdParser
from timetable_parser import TimetableParser
from saver import Saver
import settings
from mongo_client import RaspMongoClient


def main():
    id_parser = GroupIdParser('https://rasp.guap.ru/')
    id_parser.run()
    lessons = []
    loguru.logger.info(f'total ids {len(id_parser.result)}')
    for group in id_parser.result:
        ref = f'https://rasp.guap.ru/?g={group["value"]}'
        timetable_parser = TimetableParser(ref)
        timetable_parser.run()
        for lesson in timetable_parser.result:
            if lesson not in lessons:
                lessons.append(lesson)

    try:
        bd = RaspMongoClient(settings.mongo_connecting_string, settings.mongo_db_name)
        if settings.USE_DB:
            Saver.save_to_mongo(lessons, bd, settings.mongo_collection_name)
            loguru.logger.info(f'timetable successfully saved to mongoDB({settings.mongo_db_name}'
                               f'.{settings.mongo_collection_name})')
            bd.disconnect()
        else:
            Saver.save_to_json(lessons, settings.json_path)
            loguru.logger.info(f'timetable successfully saved to json({settings.json_path}')
    except Exception as _ex:
        loguru.logger.error(_ex)


if __name__ == '__main__':
    main()
