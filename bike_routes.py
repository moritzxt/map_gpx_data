
import folium
import openrouteservice
from openrouteservice import convert
import json
import branca.colormap as cm
import numpy as np
import pandas as pd
import os 


#Path of your activity files
path_gpx = "PATH"
List = os.listdir(path_gpx)



def read_json(link):

    '''
    read function to get longitude and latitude columns
    from json file. Data was exported with Golden 
    Cheetah and the Strava API
    
    read_json returns Pandas Dataframe
    '''

    link = os.path.join(path_gpx,link)
    with open(link,'r', encoding='utf-8-sig') as f:
        data = json.load(f)
        try:
            df = pd.DataFrame(data['RIDE']['SAMPLES'])
        except:
            df = pd.DataFrame()
    return df


def create_map():

    ''' creating basic map, opening up at location'''

    location = [10,52]
    m = folium.Map([location[1], location[0]], zoom_start=10)

    return m

def save_map(m, path_html = 'bike_map.html'):

    '''saving the map
        takes the map and specific 
        path_html where to save the file
        '''

    m.save(path_html)




def create_bike_map(dict):

    '''create map from dict which contains 
    for every key a Dataframe containing longitude, 
    latitude and weight of the location poit'''

    location = [10,52]#get_lat_long_from_adress('Hans-Otto-Str. 15, 10407 Berlin, Deutschland')
    m = folium.Map([location[1], location[0]], zoom_start=10)

    for key in dict:
        lat = list(dict[key]['lat'])
        long = list(dict[key]['long'])
        points = zip(lat,long)
        color = list(dict[key]['count'])
        try:
            folium.PolyLine(points, weight = 3, opacity = 1).add_to(m)
        except:
             print(f'Error to add Route {key}')
