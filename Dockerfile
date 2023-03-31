FROM python:latest

RUN pip3 install aiogram
RUN pip3 install FlightRadarAPI

CMD apt update && apt install nano iperf3

ADD main.py /FlightRadarBot/
ADD bot.py /FlightRadarBot/
ADD config.py /FlightRadarBot/
ADD flightDemon.py /FlightRadarBot/
ADD utility.py /FlightRadarBot/
ADD models/user.py /FlightRadarBot/models/
ADD SQL_scripts/database_init.sql /FlightRadarBot/SQL_scripts/

ENV TOKEN=token

WORKDIR /FlightRadarBot/

CMD python3 main.py