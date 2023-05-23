# def pois_within_radius(self):
#         pois = POI.objects.all()
#         center_lat, center_lon = radians(self.center_latitude), radians(self.center_longitude)
#         radius = self.radius_km / EARTH_RADIUS_KM  # Convert radius to radians
#         results = []
#         for poi in pois:
#             poi_lat, poi_lon = radians(poi.latitude), radians(poi.longitude)
#             d_lat, d_lon = poi_lat - center_lat, poi_lon - center_lon
#             a = sin(d_lat/2)**2 + cos(center_lat) * cos(poi_lat) * sin(d_lon/2)**2
#             c = 2 * asin(sqrt(a))
#             distance_km = EARTH_RADIUS_KM * c
#             if distance_km <= self.radius_km:
#                 results.append(poi)
#         return results