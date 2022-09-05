import loguru

from group_id_parser import GroupIdParser
from timetable_parser import TimetableParser
from saver import Saver
import settings
from mongo_client import RaspMongoClient


def main():

    bd = RaspMongoClient(settings.mongo_connecting_string, settings.mongo_db_name)

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

    if settings.USE_DB:
        Saver.save_to_mongo(lessons, bd, settings.mongo_collection_name)
    else:
        Saver.save_to_json(lessons, settings.json_path)


if __name__ == '__main__':
    main()
