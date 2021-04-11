FROM python:3.6-slim
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt
COPY . .
RUN pip install -e .
