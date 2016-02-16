import geoip2.database

reader = geoip2.database.Reader('./GeoLite2-City.mmdb')

response = reader.city('128.101.101.101')

print(response.country.name)
print(response.location.latitude)
print(response.location.longitude)