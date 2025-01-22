
"""
Created on Fri Jan 29 09:50:19 2021

@author: jboshers
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import shapely
from shapely.ops import cascaded_union
from shapely.geometry import shape, Point, Polygon, MultiPolygon
import json
import geopandas as gpd
#from geomet import wkt
import os
from shapely import wkt
import pandas as pd
def Main():
    file = os.path.join("/Users/jboshers/Desktop/","UCLA.geojson")
    with open(file,'r') as F:
        Holes = json.loads(F.read())
    file1 = os.path.join("/Users/jboshers/Downloads/","LAX_Invisible.geojson")
    with open(file1,'r') as F1:
        Area = json.loads(F1.read())
    
    z =0
    Polys = []
    y =  {"type": "FeatureCollection","features": []}
    for feature in Area['features']:
        poly = shape(feature['geometry'])
        y = gpd.GeoSeries([poly]).to_json()
       # print(y)
        y =  {"type": "FeatureCollection","features": []}
        for f in Holes['features']:
            geom = Polygon(f['geometry']['coordinates'][0])
            if poly ==geom:
                print("FOUND")
            elif poly.contains(geom) or poly.overlaps(geom):
                print("OVERLAP")
              # # print("OVERLAP", geom)
                q = geom.buffer(0.000015)
                y['features'].append(f)
                nonoverlap = (poly.symmetric_difference(q)).difference(q)
                poly = nonoverlap
        Polys.append(poly)
 
    y = gpd.GeoSeries(cascaded_union(Polys)).to_json()
    name = 'Brentwood_1'
   # print(z)
    with open('/Users/jboshers/Desktop/' + name + '.geojson', 'w') as f:   
            f.write(y)
def MultiPoly():
     multipolygon_wkt = ''
    multipolygon = wkt.loads(multipolygon_wkt)
    list_parts = []
    eps = 0.00004065638600000378
    for polygon in multipolygon.geoms:
        list_interiors = []
        for interior in polygon.interiors:
            p = Polygon(interior)
            if p.area > eps:
                list_interiors.append(interior)
        temp_pol = Polygon(polygon.exterior.coords, holes=list_interiors)
        list_parts.append(temp_pol)
        
    new_multipolygon = MultiPolygon(list_parts)
    N = gpd.GeoSeries(cascaded_union(new_multipolygon)).to_json()
    print(N)
def Poly():
    import json
    # sample polygon
    polygon_wkt = ''
    polygon = wkt.loads(polygon_wkt)
    list_interiors = []
    eps = 0.00004065638600000378
    
    for interior in polygon.interiors:
        p = Polygon(interior)   
        if p.area > eps:
            list_interiors.append(interior)
    
    new_polygon = Polygon(polygon.exterior.coords, holes=list_interiors)
    #print(new_polygon)
    N = gpd.GeoSeries(cascaded_union(new_polygon)).to_json()
    #print(N)
    poly = []
    A = new_polygon
    B = wkt.loads('POLYGON Z ((-122.73545 45.59364 0, -122.733097 45.593041 0')
    poly.append(A)
    poly.append(B)
    N = gpd.GeoSeries(cascaded_union(poly)).to_json()
    print(N)
if __name__ == "__main__":
    Main()
