
import folium
import json
import branca.colormap as cm
import numpy as np
import pandas as pd
import os 


#Path of your activity files
path_gpx = "PATH TO JSON FILES FROM GOLDEN CHEETAH USING STRAVA API TO GET ACTIVITIES"
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

def get_data(List):

    lat = []
    lon = []
    routes = {} #dict to save all routes 
    df_coords_total = pd.DataFrame() #Dataframe to save all coordinates
    k = 0 # iterating variable to get starting position for each route
    key_value = 1 #variable to generate key for routes dict

    for link in List:
        data = read_json(link)
        try:
            lon.extend(data.LON.tolist())
            lat.extend(data.LAT.tolist())
        except:
            print('Error im Dataframe', sep='|')

    
    df_coords_total['lat'] = lat
    df_coords_total['long'] = lon
    # Reducing Datapoints by rounding, less computing time, less exact
    df_coords_total['lat'] = df_coords_total['lat'].round(5) 
    df_coords_total['long'] = df_coords_total['long'].round(5)
    df_coords_total = df_coords_total.dropna()
    # Grouping same datapoints, counting the appearance of same valuepairs 
    # to create weight value for the map
    df_new = df_coords_total.groupby(by=['lat','long'], sort=False).size().to_frame('count').reset_index()



    for i in range(len(df_new)):
        if abs(df_new['lat'].iloc[i] - df_new['lat'].iloc[i-1]) > 0.01 or abs(df_new['long'].iloc[i] - df_new['long'].iloc[i-1]) > 0.01:
            '''condition checks wether the next point is 
                too far away to be from the same route so the routes can be split up'''
            routes[f'route_{key_value}'] = df_new.iloc[k:i]
            k = i
            key_value +=1

    return routes


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
    save_map(m)


if __name__ == '__main__':
    routes = get_data(List)
    create_bike_map(routes)