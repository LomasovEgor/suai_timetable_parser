import re

import loguru

from parser import Parser
from http_request_maker import HttpRequestMaker
from bs4 import BeautifulSoup as bs


class TimetableParser(Parser):
    """Loads the timetable body"""
    instances_counter: int = 0

    def __init__(self, url):
        super().__init__(url)
        self.__class__.instances_counter += 1

    @classmethod
    def get_created_instances_count(cls):
        return cls.instances_counter

    def run(self):
        if self.get_created_instances_count() == 0:
            loguru.logger.info('TimetableParser started work')
        loguru.logger.debug(f'TimetableParser is running ({self.get_created_instances_count()})')
        self.request = HttpRequestMaker.send_get_request(self.url)
        self.soup = bs(self.request.text, "html.parser")
        class_result = self.soup.find('div', class_='result')
        # group = re.search(r'(\w+) - (.*)', class_result.find('h2').text).group(2)
        self.result = self.crt_dict(class_result)

    @staticmethod
    def divide_by_days(class_result):
        days = []
        h3_tags = class_result.find_all('h3')
        for index, h3 in enumerate(h3_tags):
            day = [h3_tags[index].text]
            if index + 1 < len(h3_tags):
                while h3.find_next_sibling() != h3_tags[index + 1]:
                    nex_el = h3.find_next_sibling()
                    h3 = nex_el
                    day.append(nex_el.text)
            else:
                while h3.find_next_sibling() is not None:
                    nex_el = h3.find_next_sibling()
                    h3 = nex_el
                    day.append(nex_el.text)
            days.append(day)
        return days

    def crt_dict(self, class_result):
        days = self.divide_by_days(class_result)
        lessons = []

        for day in days:
            day_name = day[0]
            start_time = ''
            end_time = ''
            lesson_number = ''
            for string in day[1:]:
                if 'пара (' in string:
                    match = re.search(r'(.*) пара \((.*)–(.*)\)', string)
                    lesson_number = match.group(1)
                    start_time = match.group(2)
                    end_time = match.group(3)
                elif 'вне сетки' in string:
                    start_time = ''
                    end_time = ''
                    lesson_number = 'Вне сетки расписания'
                else:
                    time_lessons = self.expand_lesson(string) if isinstance(string, str) else string
                    lesson = {
                        'week_day': day_name,
                        'start_time': start_time,
                        'end_time': end_time,
                        'lesson_number': lesson_number
                    }
                    lesson.update(time_lessons)
                    lessons.append(lesson)
        return lessons

    @staticmethod
    def expand_lesson(lesson: str) -> dict:
        match = re.search(r'(.*)(ЛР|Л|ПР|КР|КП)\W*(.*)  \W*(.*), ауд. (.*)(Группы: |Группа: )(.*)', lesson)

        if match.group(1) == '':
            week_type = ['верхняя', 'нижняя']
        elif match.group(1) == '▲ ':
            week_type = ['верхняя']
        elif match.group(1) == '▼ ':
            week_type = ['нижняя']
        else:
            week_type = ['неопределено']
        lesson_type = match.group(2)
        lesson_name = match.group(3)
        building = match.group(4)
        class_room_and_teacher = match.group(5)
        if ':' in class_room_and_teacher:
            match2 = re.search(r'(.*)(Преподаватель: |на базе кафедры |Преподаватели: )(.*)', class_room_and_teacher)
            class_room = [room.strip() for room in match2.group(1).split(sep=';')]
            teachers = [teacher.strip() for teacher in match2.group(3).split(sep=';')]
        else:
            class_room = [room.strip() for room in match.group(5).split(sep=';')]
            teachers = ['']
        groups = re.findall(r'\w+', match.group(7))

        expanded_lesson = {
            'week_types': week_type,
            'lesson_type': lesson_type,
            'lesson_name': lesson_name,
            'building': building,
            'class_rooms': class_room,
            'teachers': teachers,
            'groups': groups,
        }

        return expanded_lesson
