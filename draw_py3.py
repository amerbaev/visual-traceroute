import json
import random
import math

def generate(j_list):
    file = '<!DOCTYPE html><html><head></head><body><script src="http://cdnjs.cloudflare.com/ajax/libs/d3/3.5.3/d3.min.js"></script><script src="http://cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js"></script><script src="./datamaps.world.min.js"></script><div id="container" style="position: relative; width: 500px; height: 300px;"></div><script>var map = new Datamap({element: document.getElementById("container"), fills: {defaultFill: "rgba(200,200,200,1)"},height: 700,width: 1300,setProjection: function(element) { var projection = d3.geo.equirectangular() .center([-40, 60]) .rotate([4.4, 0])   .scale(450); var path = d3.geo.path() .projection(projection); return {path: path, projection: projection};},});map.arc('
    k = json.loads(j_list)
    arc = list()
    for i in k:
        r = random.randint(50, 255)
        g = int(math.fmod(r + 122, 256))
        b = random.randint(50, 255)
        print(r, g, b)
        for key,j in enumerate(i['hops']):
            if key>0:
                if round(i['hops'][key-1]['lat']) != round(j['lat']) or round(i['hops'][key-1]['lon']) != round(j['lon']):
                    unit = {'origin': {
                                'latitude': i['hops'][key-1]['lat'],
                                'longitude' : i['hops'][key-1]['lon']
                                },
                            'destination': {
                                'latitude': j['lat'],
                                'longitude' : j['lon']
                            },
                            'options': {
                                'strokeColor': '\'rgba(' + str(r) + ', ' + str(g) + ', ' + str(b) + ', 1)\'',
                            }
                        }
                    arc.append(unit)
                    print('Origin_Lat', i['hops'][key-1]['lat'], 'Origin_Lon', i['hops'][key-1]['lon'])
                    print('Dest_Lat', j['lat'], 'Dest_Lon', j['lon'])
    res = json.dumps(arc)
    res = res.replace('"','')

    res = file+res+',{strokeWidth: 1.5, arcSharpness: 0.5});</script></body></html>'

    f = open('test.html','w')
    f.write(res)
    f.close()