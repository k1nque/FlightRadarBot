from math import sin, cos, acos, pi
from models.user import EarthRadius




def getShortestDistance(latitude, longitude, lat: float, lon: float) -> float:
    cos_angle: float = sin(latitude*pi/180) * sin(lat*pi/180) + cos(latitude*pi/180) * cos(lat*pi/180) * cos(
        (lon - longitude)*pi/180)
    return acos(cos_angle)  * EarthRadius


print(getShortestDistance(40.44004434595748, -3.6900487472024732, 56.03271953490631, 37.624168865424565))