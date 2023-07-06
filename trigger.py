import pandas as pd

import pyarrow

import fsspec

import gcsfs

def trigger_function(request):

  df_link = pd.read_csv('https://celestrak.com/NORAD/elements/gp.php?GROUP=active&FORMAT=csv')

  df_storage = pd.read_parquet('gs://active-satellites/active satellites.parquet', engine = 'pyarrow')

  if df_link.equals(df_storage):
    
    pass
    
  else:
    
    df_link.to_parquet('gs://active-satellites/active satellites.parquet', engine = 'pyarrow')
    
  return 'check completed successfully'