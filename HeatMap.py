#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 23:29:36 2020

@author: jboshers
"""


import json
import os
import geojson
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, shape
from polygon_geohasher.polygon_geohasher import polygon_to_geohashes, geohash_to_polygon, geohashes_to_polygon
from colour import Color
import sys
import requests
from github import Github
from google.cloud import secretmanager


def convert_to_rgb(Min, Max, Value):
      
    Mid = (Min + Max) / 2
    if Min <= Value <= Mid:
        r = 0
        g = int( 255/(halfmax - minimum) * (value - minimum))
        b = int( 255 + -255/(Mid - Min)  * (Value - Min))
        return (r,g,b)    
    elif Mid < Value <= Max:
        r = int( 255./(Max - Mid) * (Value - Mid))
        g = int( 255. + -255./(Max - Mid)  * (Value - Mid))
        b = 0
        return (r,g,b)   
def UploadFile(FileNm,Desc,Code):

    token = get_secret(GITHUB_Key)
    g = Github(token)
    g.load
    for repo in g.get_user().get_repos():
        if repo.name == 'Sample':
            repo.create_file(FileNm, Desc, json.dumps(Code), branch="master")
    

def CreateJsonFile(df,column,File):
  Geo = {"type": "FeatureCollection","features": []}
  for index,row in df.iterrows():
      
      geo = row[column]
      x = geohash_to_polygon(geo)
      print(index)
      df.at[index,'geometry'] = x
      x = gpd.GeoSeries([x]).to_json()     
      x = json.loads(x)
      feature = {}
      feature['type'] = 'Feature'
      feature['geometry'] = x['features'][0]['geometry']
      feature['properties'] = {"id": row['geo8'],'neighborhood':row['Neighborhood']}     
      feature['properties'] = { "fill": row['hex_color'], "fill-opacity": 0.3,"geohash": row['geo7'], "Rides":row['Rides']}
      Geo['features'].append(feature)

  return Geo
def FindServiceArea(Lat,Lng):
    Area = '{}'
    Area = json.loads(Area)
    point = Point(Lng, Lat)
    Found = False
    for feature in Area['features']:     
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            Found = True
            return feature['properties']['id']
    if Found==False:
        return 'OutofArea'  

def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    project_id = "TBD"  # Replace with your project ID
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")
    
if __name__ == "__main__":
    token = get_secret(Mapbox_Token)
    df = Dataset[0]
    Name = 'HeatMap_' + datetime.now().strftime("%Y-%m-%d")
    desc = "Daily Heat Map of Rides Started" 
    dMax = float(df.Rides.max())
    dMin = float(df.Rides.min())
    for index,row in df.iterrows():
        value = row['Rides']
        df.at[index,'hex_color'] =  convert_to_rgb(dMin,dMax,value)
    
    Json_File = CreateJsonFile(df,'geo8',File)
    UploadFile(Name ,desc ,Json_File)




