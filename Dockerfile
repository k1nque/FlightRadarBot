FROM python:latest

RUN pip3 install aiogram
RUN pip3 install FlightRadarAPI

ADD main.py /FlightRadarBot/
ADD bot.py /FlightRadarBot/
ADD config.py /FlightRadarBot/
ADD flightDemon.py /FlightRadarBot/
ADD utility.py /FlightRadarBot/
ADD models/user.py /FlightRadarBot/models/
ADD SQL_scripts/database_init.sql /FlightRadarBot/SQL_scripts/

ENV TOKEN=5996986939:AAFqhpZ03H7t1NJl-EYS7n7v72WK2mzI99A

WORKDIR /FlightRadarBot/

CMD python3 main.py -c && python3 main.py