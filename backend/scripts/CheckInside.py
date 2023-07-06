from math import radians, cos, sin, asin, sqrt

EARTH_RADIUS_KM = 6371

def pois_within_radius(self,pois, savedsearch):
        center_lat, center_lon = radians(savedsearch.CenterLatitude), radians(savedsearch.CenterLongitude)
        results = []
        for poi in pois:
            poi_lat, poi_lon = radians(poi.Latitude), radians(poi.Longitude)
            d_lat, d_lon = poi_lat - center_lat, poi_lon - center_lon
            a = sin(d_lat / 2) ** 2 + cos(center_lat) * cos(poi_lat) * sin(d_lon / 2) ** 2
            c = 2 * asin(sqrt(a))
            distance_km = EARTH_RADIUS_KM * c
            if distance_km <= savedsearch.Radius:
                results.append(poi)
        return results