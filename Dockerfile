FROM python:latest

ENV TOKEN=5996986939:AAEzsuEMr8TvPL65XBZvYyiX00ujv87QnUI
RUN pip3 install aiogram
RUN pip3 install FlightRadarAPI

ADD main.py /FlightRadarBot/
    ADD bot.py /FlightRadarBot/
ADD config.py /FlightRadarBot/
ADD flightDemon.py /FlightRadarBot/
ADD utility.py /FlightRadarBot/
ADD models/user.py /FlightRadarBot/models/
ADD SQL_scripts/database_init.sql /FlightRadarBot/SQL_scripts/

WORKDIR /FlightRadarBot/

CMD python3 main.py -c && python3 main.py