# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
#COPY telegrambot/bot.py /code/
# COPY applications/bot/bot.py ./
#CMD python3 telegrambot/bot.py
RUN pip install -r requirements.txt
#CMD python bot.py
