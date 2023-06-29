
import fsspec

import gcsfs

import numpy as np

import pandas as pd

import pyarrow

import yaml

from alert import *

from data_validation import *

def etl_function(event, context):

  try:

    with open('config.yaml', 'r') as file:

      config = yaml.safe_load(file)

    weather_sat_list = config['weather_sat_links']

    earth_observation_sat_list = config['earth_observation_sat_links']

    communications_sat_list = config['communications_sat_links']

    navigation_sat_list = config['navigation_sat_links']

    scientific_sat_list = config['scientific_sat_links']

    miscellaneous_sat_list = config['miscellaneous_sat_links']
    
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

    data_validation(active_sat_leo_df)

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

    data_validation_2(active_sat_leo_df2)

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

    earth_observation_sat_df = sat_class_data(earth_observation_sat_list)     

    communications_sat_df = sat_class_data(communications_sat_list)

    navigation_sat_df = sat_class_data(navigation_sat_list)

    scientific_sat_df = sat_class_data(scientific_sat_list)

    miscellaneous_sat_df = sat_class_data(miscellaneous_sat_list)

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

    active_leo_satellites = drop_duplicates2()

    data_validation_2(active_leo_satellites)

    active_leo_satellites_mod1 = active_leo_satellites['YearOfLaunch'].value_counts().rename_axis('YearOfLaunch').reset_index(name = 'Counts').sort_values(by = ['YearOfLaunch'])

    active_leo_satellites_mod2 = active_leo_satellites.groupby('YearOfLaunch')['Purpose'].value_counts().rename_axis(['YearOfLaunch','Purpose']).reset_index(name = 'Counts')

    def store_data(df, name):

        return df.to_parquet(f'gs://active-leo-satellites/{name}.parquet', engine = 'pyarrow')

    store_data(active_leo_satellites, 'active leo satellites')

    store_data(active_leo_satellites_mod1, 'active leo satellites mod1')

    store_data(active_leo_satellites_mod2, 'active leo satellites mod2')

    send_email('The ETL function run was successful')

  except Exception as e:

    send_email(f'a {e} has occurred')
