from google.cloud import storage

import pandas as pd

import numpy as np

from datetime import datetime

import xlrd

import openpyxl

import fsspec

import gcsfs

import functions_framework

@functions_framework.http

def active_leo_sat(request):
  
  def read_data():
    
    """Reads the active satellite data csv file link 
    
    into a active satellites DataFrame"""
    
    active_sat_df = pd.read_csv('https://celestrak.com/NORAD/elements/gp.php?GROUP=active&FORMAT=csv')
    
    return active_sat_df

  active_sat_df = read_data()

  def filter_data():
    
    """Filters out the active satellites in Low Earth Orbit
    
    out of the active satellites DataFame and reset the index 
    
    of the new DataFrame"""
    
    active_sat_leo_df = active_sat_df.loc[(active_sat_df['MEAN_MOTION']>=11.25) & (active_sat_df['ECCENTRICITY']<0.25)]
    
    active_sat_leo_df.reset_index(drop = True, inplace = True)
    
    return active_sat_leo_df

  active_sat_leo_df = filter_data()

  def drop_columns():
    
    """Drops Unwanted columns in the active satellites in Low Earth 
    
    Orbit DataFrame"""
    
    active_sat_leo_df1 = active_sat_leo_df.drop(
        
        active_sat_leo_df.loc[:,'EPOCH':'MEAN_MOTION_DDOT'], axis = 1)
    
    return active_sat_leo_df1

  active_sat_leo_df1 = drop_columns()

  def extract_replace():
    
    """Extract the year the satellite was launched from
    
    the object_id column and replace the object id data
    
    with the year data"""
    
    for object_id in active_sat_leo_df1['OBJECT_ID']:
        
        if '-' in object_id:
            
            index = object_id.find('-')
            
            object_id_slice = object_id[0:index]
            
            active_sat_leo_df1['OBJECT_ID'] = active_sat_leo_df1['OBJECT_ID'].replace(
            
            to_replace = object_id, value = object_id_slice)
            
    return active_sat_leo_df1

  active_sat_leo_df1 = extract_replace()

  def rename_columns():
    
    """Rename the Columns of the DataFrame"""
    
    active_sat_leo_df1.columns = ['ObjectName', 'YearOfLaunch']
    
    return active_sat_leo_df1

  active_sat_leo_df1 = rename_columns()

  def drop_duplicates():
    
    """Drop duplicates if any from the DataFrame
    
    and reset index"""
    
    active_sat_leo_df2 = active_sat_leo_df1.drop_duplicates()
    
    active_sat_leo_df2.reset_index(drop = True, inplace = True)
    
    return active_sat_leo_df2

  active_sat_leo_df2 = drop_duplicates()

  #Collects satellites csv file links based on the purpose into lists 

  weather_sat_list = ['https://celestrak.com/NORAD/elements/gp.php?GROUP=weather&FORMAT=csv',
                    
                    'https://celestrak.com/NORAD/elements/gp.php?GROUP=noaa&FORMAT=csv',
                    
                    'https://celestrak.com/NORAD/elements/gp.php?GROUP=goes&FORMAT=csv']


  earth_observation_sat_list = ['https://celestrak.com/NORAD/elements/gp.php?GROUP=resource&FORMAT=csv',
                              
                              'https://celestrak.com/NORAD/elements/gp.php?GROUP=sarsat&FORMAT=csv',
                              
                              'https://celestrak.com/NORAD/elements/gp.php?GROUP=dmc&FORMAT=csv',
                              
                              'https://celestrak.com/NORAD/elements/gp.php?GROUP=tdrss&FORMAT=csv',
                              
                              'https://celestrak.com/NORAD/elements/gp.php?GROUP=argos&FORMAT=csv',
                              
                              'https://celestrak.com/NORAD/elements/gp.php?GROUP=planet&FORMAT=csv',
                              
                              'https://celestrak.com/NORAD/elements/gp.php?GROUP=spire&FORMAT=csv']


  communications_sat_list = ['https://celestrak.com/NORAD/elements/gp.php?GROUP=intelsat&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=ses&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=iridium&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=iridium-NEXT&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=starlink&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=oneweb&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=orbcomm&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=globalstar&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=swarm&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=amateur&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=x-comm&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=other-comm&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=satnogs&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=gorizont&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=raduga&FORMAT=csv',
                  
                  'https://celestrak.com/NORAD/elements/gp.php?GROUP=molniya&FORMAT=csv']

  navigation_sat_list = ['https://celestrak.com/NORAD/elements/gp.php?GROUP=gnss&FORMAT=csv',
                
                'https://celestrak.com/NORAD/elements/gp.php?GROUP=gps-ops&FORMAT=csv',
                
                'https://celestrak.com/NORAD/elements/gp.php?GROUP=glo-ops&FORMAT=csv',
                
                'https://celestrak.com/NORAD/elements/gp.php?GROUP=galileo&FORMAT=csv',
                
                'https://celestrak.com/NORAD/elements/gp.php?GROUP=beidou&FORMAT=csv',
                
                'https://celestrak.com/NORAD/elements/gp.php?GROUP=sbas&FORMAT=csv',
                
                'https://celestrak.com/NORAD/elements/gp.php?GROUP=nnss&FORMAT=csv',
                
                'https://celestrak.com/NORAD/elements/gp.php?GROUP=musson&FORMAT=csv']

  scientific_sat_list = ['https://celestrak.com/NORAD/elements/gp.php?GROUP=science&FORMAT=csv',
                    
                    'https://celestrak.com/NORAD/elements/gp.php?GROUP=geodetic&FORMAT=csv',
                    
                    'https://celestrak.com/NORAD/elements/gp.php?GROUP=engineering&FORMAT=csv',
                    
                    'https://celestrak.com/NORAD/elements/gp.php?GROUP=education&FORMAT=csv']

  miscellaneous_sat_list = ['https://celestrak.com/NORAD/elements/gp.php?GROUP=military&FORMAT=csv',
                          
                          'https://celestrak.com/NORAD/elements/gp.php?GROUP=radar&FORMAT=csv',
                          
                          'https://celestrak.com/NORAD/elements/gp.php?GROUP=cubesat&FORMAT=csv',
                          
                          'https://celestrak.com/NORAD/elements/gp.php?GROUP=other&FORMAT=csv']

  def sat_class_data(sat_list):
    
    """Takes sat_list as an argument which is a list data structure 
    
    containing satellite csv file links, read the data in the list 
    
    and join the data to an empty DataFrame df"""
    
    df = pd.DataFrame()
    
    for url in sat_list:
        
        sats_df = pd.read_csv(url)
        
        df = pd.concat([df, sats_df])
        
    df.reset_index(drop = True, inplace = True) #reset the index of the DataFrame
    
    df = df.drop(df.loc[:,'OBJECT_ID':'MEAN_MOTION_DDOT'], axis = 1) #drops unwanted columns of the DataFrame
    
    df.columns = ['ObjectName'] #rename the column name of the Series
    
    return df

  #Obtains data for each of the lists defined above and create a new column purpose

  weather_sat_df = sat_class_data(weather_sat_list)

  weather_sat_df['Purpose'] = 'Weather'

  earth_observation_sat_df = sat_class_data(earth_observation_sat_list)

  earth_observation_sat_df['Purpose'] = 'Earth Observation'      

  communications_sat_df = sat_class_data(communications_sat_list)

  communications_sat_df['Purpose'] = 'Communications'

  navigation_sat_df = sat_class_data(navigation_sat_list)

  navigation_sat_df['Purpose'] = 'Navigation' 

  scientific_sat_df = sat_class_data(scientific_sat_list)

  scientific_sat_df['Purpose'] = 'Scientific'  

  miscellaneous_sat_df = sat_class_data(miscellaneous_sat_list)

  miscellaneous_sat_df['Purpose'] = 'Miscellaneous' 

  def join_sat_list():
    
    """join all the data from each category(purpose) 
    
    into one master DataFrame and reset the index"""
    
    
    master_df = pd.concat([weather_sat_df, earth_observation_sat_df, 
                           
                           communications_sat_df, navigation_sat_df, 
                           
                           scientific_sat_df, miscellaneous_sat_df])
    
    master_df.reset_index(drop = True, inplace = True)
    
    return master_df

  master_df = join_sat_list()

  def merge_data():
    
    """Merge both the active low earth orbit satellites 
    
    DataFrame active_sat_leo_df2 and the master DataFrame
    
    master_df into one DataFrame active_sat_leo_df3"""
    
    active_sat_leo_df3 = pd.merge(active_sat_leo_df2, master_df, how ='left', on =['ObjectName'])
    
    return active_sat_leo_df3

  active_sat_leo_df3 = merge_data()

  def replace_nan():
    
    """Replace NaN values in the Purpose Column with
    
    Miscellaneous"""
    
    active_sat_leo_df3['Purpose'] = active_sat_leo_df3['Purpose'].replace(np.nan, 'Miscellaneous')
    
    return active_sat_leo_df3

  active_sat_leo_df3 = replace_nan()

  def drop_duplicates2():
    
    """Drop duplicates if any from the DataFrame
    
    and reset index"""
    
    active_sat_leo_df4 = active_sat_leo_df3.drop_duplicates(subset = 'ObjectName')
    
    active_sat_leo_df4.reset_index(drop = True, inplace = True)
    
    return active_sat_leo_df4

  active_sat_leo_df4 = drop_duplicates2()

  def store_data():
    
    return active_sat_leo_df4.to_csv('gs://active-leo-satellites/active leo satellites.csv')
    
  store_data()

  return 'Function ran successfully'
