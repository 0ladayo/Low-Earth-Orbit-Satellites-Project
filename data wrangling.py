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

  active_sat_df = pd.read_csv('https://celestrak.com/NORAD/elements/gp.php?GROUP=active&FORMAT=csv')

  active_leo_sat_df = active_sat_df.loc[(active_sat_df['MEAN_MOTION']>=11.25) & (active_sat_df['ECCENTRICITY']<0.25)] 
  
  active_leo_sat_df.reset_index(drop = True, inplace = True)

  active_leo_sat_df = active_leo_sat_df.drop(active_leo_sat_df.loc[:,'EPOCH':'MEAN_MOTION_DDOT'], axis = 1)

  for object_id in active_leo_sat_df['OBJECT_ID']:
    
    if '-' in object_id:
        
        index = object_id.find('-')
        
        object_id_format = object_id[0:index]
        
        active_leo_sat_df['OBJECT_ID'] = active_leo_sat_df['OBJECT_ID'].replace(to_replace = object_id, value = object_id_format)
        
    else:
        
        pass

  active_leo_sat_df.columns = ['ObjectName', 'YearOfLaunch']
  
  active_leo_sat_df = active_leo_sat_df.drop_duplicates(subset = 'ObjectName')
  
  active_leo_sat_df.reset_index(drop = True, inplace = True)

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
                
  def sat_classification(sat_list):
    
    df = pd.DataFrame()
    
    for url in sat_list:
        
        sats_df = pd.read_csv(url)
        
        df = pd.concat([df, sats_df])
        
    df.reset_index(drop = True, inplace = True)
    
    df = df.drop(df.loc[:,'OBJECT_ID':'MEAN_MOTION_DDOT'], axis = 1)
    
    df.columns = ['ObjectName']
    
    return df
  
  weather_sat_df = sat_classification(weather_sat_list)

  weather_sat_df['Purpose'] = 'Weather'

  earth_observation_sat_df = sat_classification(earth_observation_sat_list)

  earth_observation_sat_df['Purpose'] = 'Earth Observation'

  communications_sat_df = sat_classification(communications_sat_list)

  communications_sat_df['Purpose'] = 'Communications'

  navigation_sat_df = sat_classification(navigation_sat_list)

  navigation_sat_df['Purpose'] = 'Navigation'

  scientific_sat_df = sat_classification(scientific_sat_list)

  scientific_sat_df['Purpose'] = 'Scientific'

  miscellaneous_sat_df = sat_classification(miscellaneous_sat_list)

  miscellaneous_sat_df['Purpose'] = 'Miscellaneous'

  master_df = pd.concat([weather_sat_df, earth_observation_sat_df, communications_sat_df, navigation_sat_df, scientific_sat_df, miscellaneous_sat_df])

  master_df.reset_index(drop = True, inplace = True)

  active_leo_sat_df = pd.merge(active_leo_sat_df, master_df, how ='left', on =['ObjectName'])

  active_leo_sat_df['Purpose'] = active_leo_sat_df['Purpose'].replace(np.nan, 'Others')

  active_leo_sat_df = active_leo_sat_df.drop_duplicates(subset = 'ObjectName')

  active_leo_sat_df.reset_index(drop = True, inplace = True)

  active_leo_sat_df.to_csv('gs://active-leo-satellites/active leo satellites.csv', index = False)

  return 'Function ran successfully'
