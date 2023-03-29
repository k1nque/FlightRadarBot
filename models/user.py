from json import loads, dumps
from math import sin, cos, acos, pi
from FlightRadar24.flight import Flight
from FlightRadar24.api import FlightRadar24API
from config import EPS

EarthRadius = 6370


class User:
    def __init__(self, userFieldsList):
        self.UID = userFieldsList[0]
        self.__user_state = loads(userFieldsList[1])
        if userFieldsList[2] is not None:
            self.__latitude = userFieldsList[2]
            self.__longitude = userFieldsList[3]
        if userFieldsList[4] is not None:
            self.__distanceThreshold = userFieldsList[4]
        if userFieldsList[5] is not None:
            self.__notified: list[str] = loads(userFieldsList[5])
        else:
            self.__notified: list[str] = []
        self.__api = FlightRadar24API()

    @property
    def isReady(self) -> bool:
        return self.__user_state['READY']

    @property
    def notified(self) -> str:
        return dumps(self.__notified)

    def __getFlights(self) -> list[Flight]:
        try:
            flights: list[Flight] = self.__api.get_flights(
                bounds=f'{self.__latitude + EPS},{self.__latitude - EPS},{self.__longitude - EPS},{self.__longitude + EPS}')
            return flights
        except Exception as ex:  # TODO do nice exception check
            print(ex)

    def getNearAircrafts(self) -> list[Flight]:
        toNotifyIds: list[str] = []
        toNotify: list[Flight] = []

        flights = self.__getFlights()

        if flights is not None:
            for flight in flights:
                distance = self.__getShortestDistance(flight.latitude, flight.longitude)
                if distance <= self.__distanceThreshold:
                    if flight.id not in self.__notified:
                        toNotify.append(flight)
                    toNotifyIds.append(flight.id)

        self.__notified = toNotifyIds
        return toNotify

    @staticmethod
    def GetShortestDistance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        lat1 = lat1 * pi / 180
        lon1 = lon1 * pi / 180
        lat2 = lat2 * pi / 180
        lon2 = lon2 * pi / 180

        cos_angle: float = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)
        return acos(cos_angle) * EarthRadius

    def __getShortestDistance(self, lat, lon):
        return self.GetShortestDistance(self.__latitude, self.__longitude, lat, lon)
