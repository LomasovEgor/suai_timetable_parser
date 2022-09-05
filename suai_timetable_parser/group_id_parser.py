from parser import Parser
import re
from loguru import logger
from bs4 import BeautifulSoup as bs
from http_request_maker import HttpRequestMaker


class GroupIdParser(Parser):
    """Loads the timetable params"""

    def __init__(self, url):
        super().__init__(url)
        self.ids: list | None = None

    def run(self):
        logger.info('GroupIdParser is running')
        self.request = HttpRequestMaker.send_get_request(self.url)
        self.soup = bs(self.request.text, "html.parser")
        self.ids = self.soup.find('div', class_='form').find('select')
        self.result = self._unpack_param(self.ids)

    def save(self):
        pass

    @staticmethod
    def _unpack_param(string) -> list[dict]:
        """
        Returns unpacked values

        :param string: str like <option value="19">1011</option> ... <option value="352">Агеев М.П. - ассистент</option>
        :return list with dictionaries that look like: {'value': value, 'text': text}
        :rtype list
        """
        table = []
        regexp = r'<option value="(.*)".*>(.*)<.*'
        for sub_string in string:
            match = (re.search(regexp, str(sub_string)))
            if match is not None:
                value = int(match.group(1))
                text = str(match.group(2))
                table.append(
                    {'value': value,
                     'text': text}
                )
        return table
