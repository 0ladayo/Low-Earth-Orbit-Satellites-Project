import pandera as pa

from pandera import Check, Column, DataFrameSchema

def data_validation(df):
    
    schema = pa.DataFrameSchema(

    columns = {

        'MEAN_MOTION': Column(float, Check.greater_than_or_equal_to(11.25)),

        'ECCENTRICITY': Column(float, Check.less_than(0.25))
        
        },
        
        )
    
    return schema.validate(df, lazy= True)

def data_validation_2(df):

    schema = pa.DataFrameSchema(

        checks = [pa.Check(lambda df: not df.duplicated().any(), element_wise = False, error= 'DataFrame has duplicates')]


    )
   
    return schema.validate(df)