
FROM python:latest

WORKDIR /server

COPY ./requirements.txt /server/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt


COPY ./src /server/src
CMD ["fastapi", "run", "src/main.py", "--host" , "0.0.0.0", "--port", "8000"]