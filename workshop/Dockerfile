FROM python:3.10

WORKDIR /code

RUN apt-get update -y

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src /code/src
COPY data /code/data
COPY setup.py /code/setup.py
RUN pip install .