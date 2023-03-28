from FlightRadar24.api import FlightRadar24API
from config import eps, distance
import sqlite3

#
# lat, lon = 41.68, 44.82
#
#
#
#
#
# y1, y2, x1, x2 = lat + eps, lat - eps, lon - eps, lon + eps
# flights = api.get_flights(bounds=f'{y1},{y2},{x1},{x2}')
# print(len(flights))
# print(type(flights[0]))

def getUserList():
    pass


def requesting(userList):
    pass

if __name__ == "__main__":
    api = FlightRadar24API()