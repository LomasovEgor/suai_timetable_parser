FROM python:3.10
WORKDIR /src
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/suai_timetable_parser
ENTRYPOINT [ "python3", "suai_timetable_parser.main.py" ]
