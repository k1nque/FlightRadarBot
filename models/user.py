from json import loads, dumps
from math import sin, cos, acos, pi
from FlightRadar24.flight import Flight
from FlightRadar24.api import FlightRadar24API
from config import EPS

EarthRadius = 6370


class User:
    def __init__(self, userDict):
        self.UID = userDict[0]
        self.__user_state = userDict[1]
        self.__latitude = userDict[2] * pi / 180
        self.__longitude = userDict[3] * pi / 180
        self.__distanceThreshold = userDict[4]
        if userDict[5] is not None:
            self.__notified: list[str] = loads(userDict[5])
        else:
            self.__notified: list[str] = []
        self.__api = FlightRadar24API()

    @property
    def notified(self) -> str:
        return dumps(self.__notified)

    def __getFlights(self) -> list[Flight]:
        try:
            print('hujhujhuj')
            flights: list[Flight] = self.__api.get_flights(
                bounds=f'{self.__latitude + EPS},{self.__latitude - EPS},{self.__longitude + EPS}, {self.__longitude - EPS}')
            return flights
        except Exception as ex:  # TODO do nice exception check
            print(ex)

    def getNearAircrafts(self) -> list[Flight]:
        toNotifyIds: list[str] = []
        toNotify: list[Flight] = []
        print('huj1')
        flights = self.__getFlights()
        print('huj2')
        if flights is not None:
            print('huj')
            for flight in flights:
                if flight.id in self.__notified:
                    toNotifyIds.append(flight.id)
                    continue
                distance = self.__getShortestDistance(flight.latitude, flight.longitude)
                if distance <= self.__distanceThreshold:
                    toNotifyIds.append(flight.id)
                    toNotify.append(flight)
        self.__notified = toNotifyIds
        return toNotify

    def __getShortestDistance(self, lat: float, lon: float) -> float:
        lat = lat * pi / 180
        lon = lon * pi / 180
        cos_angle: float = sin(self.__latitude) * sin(lat) + cos(self.__latitude) * cos(lat) * cos(
            lon - self.__longitude)
        return acos(cos_angle) * EarthRadius
