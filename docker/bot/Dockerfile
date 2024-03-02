# Use Python 3.11 slim image as the base
FROM python:3.11
WORKDIR /usr/src/app
RUN apt-get update && \
    apt-get install -y git \
    python-is-python3 \
    python3-dev \
    lsb-release \
    libpq-dev \
    gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install pytz "python-telegram-bot[ext]" psycopg2
RUN git clone https://github.com/vazome/redbull-tracker-ge.git
RUN apt update
CMD python3 /usr/src/app/redbull-tracker-ge/Telegram/bot.py
