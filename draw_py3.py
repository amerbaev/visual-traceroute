import json
file = '<!DOCTYPE html><html><head></head><body><script src="http://cdnjs.cloudflare.com/ajax/libs/d3/3.5.3/d3.min.js"></script><script src="http://cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js"></script><script src="./datamaps.world.min.js"></script><div id="container" style="position: relative; width: 500px; height: 300px;"></div><script>var map = new Datamap({element: document.getElementById("container"), fills: {defaultFill: "rgba(50,50,156,1)"},height: 700,width: 1300});map.arc('
# [ "address": "192.168.9.9", "hops": [{"ip": "192.168.9.9", "lat": "40.639722", "lon": "-73.778889"}, {"ip": "192.168.9.1", "lat": "150.639722", "lon": "-25.778889"}, {"ip": "192.168.9.30", "lat": "255.639722", "lon": "150.778889"}] ]
str = '[ {"address": "192.168.9.9", "hops": [{"ip": "192.168.9.9", "lat": "40.639722", "lon": "-15.778889"}, {"ip": "192.168.9.1", "lat": "50.639722", "lon": "-60.778889"}, {"ip": "192.168.9.30", "lat": "30.639722", "lon": "-60.778889"}]}]'
k = json.loads(str)
arc = list()
for i in k:
	for key,j in enumerate(i['hops']):
		if key>0:
			unit = {'origin': {
							'latitude': i['hops'][key-1]['lat'],
							'longitude' : i['hops'][key-1]['lon']
							},
					 'destination': {
							'latitude': j['lat'],
							'longitude' : j['lon']
						}
					}
			arc.append(unit)
res = json.dumps(arc)
res = res.replace('"','')

res = file+res+',{strokeWidth: 3, arcSharpness: 1.4});</script></body></html>'

f = open('test.html','w')
f.write(res)
f.close()