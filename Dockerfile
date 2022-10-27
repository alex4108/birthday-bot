FROM python:3.9
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
COPY quotes.json /app/
COPY birthday-bot.py /app/
RUN mkdir /app/common
COPY common/initLogger.py /app/common/
RUN pip3 install -r requirements.txt
CMD python3 birthday-bot.py