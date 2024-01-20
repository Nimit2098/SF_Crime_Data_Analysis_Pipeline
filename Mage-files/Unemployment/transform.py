import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df_unemployment, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    #Init of a dataframe for the dimension table
    df_date = pd.DataFrame(pd.date_range(start='2018-01-01 00:01:00', end='2023-11-22 23:00:00', freq="D", inclusive='both'))
    #creating a primary key column using index of the dataframe
    df_date['Id'] = df_date.index
    #extracting date from the datetime value
    df_date['Date'] = df_date[0].dt.date
    #dropping unnecessary columns
    df_date.drop(columns=[0], inplace=True)
    #to convert the column to date type format
    df_date['Date'] = pd.to_datetime(df_date['Date'])
    #To exrtact various tangents from the date columns.
    df_date['Dayofmonth'] = df_date['Date'].dt.day
    df_date['Month_Number'] = df_date['Date'].dt.month
    df_date['Month_Name'] = df_date['Date'].dt.month_name()
    df_date['Dayofweek_number'] = df_date['Date'].dt.day_of_week
    df_date['Dayofweek_name'] = df_date['Date'].dt.day_name()
    df_date['Year'] = df_date['Date'].dt.year

    #Changing names of columns to insert Underscore in spaces and strip the blank space in the end
    df_unemployment.rename(columns=lambda x: x.strip().replace(" ","_"),inplace=True)
    #drop unnecessary columns
    df_unemployment.drop(columns=['Status_(Preliminary_/_Final)', 'Month'], inplace=True)
    #Convert the format of date column to datetime
    df_unemployment['Date'] = pd.to_datetime(df_unemployment['Date'])

    #Init of a dict for area code-name
    area_code_dict = {'Area_code' : ['0', '1'],
                    'Area_Name' : ['San Francisco County', 'California']}
    #Converting dict to dataframe
    df_area_code = pd.DataFrame.from_dict(area_code_dict)

    #fitler the unemployment dataframe for San Francisco County Area
    df_county_unemployment  = df_unemployment[((df_unemployment['Area_Name'] == 'San Francisco County') | ((df_unemployment['Area_Name'] == 'California') & (df_unemployment['Seasonally_Adjusted_(Y/N)'] == 'Y'))) & (df_unemployment['Year'] >= 2018)].copy()
    #reset the index of the fitlered dataframe
    df_county_unemployment.reset_index(inplace=True)
    #mapping the id(primary key) of dimension tables to the fact table
    df_county_unemployment['Date_Id'] = df_county_unemployment['Date'].map(df_date.set_index('Date')['Id'])
    #mapping the area name from the dimension table
    df_county_unemployment['Area_code'] = df_county_unemployment['Area_Name'].map(df_area_code.set_index('Area_Name')['Area_code'])
    #drop unnecessary columns in the dataframe
    df_county_unemployment.drop(columns=['index', 'Area_Type', 'Year', 'Date', 'Area_Name', 'Seasonally_Adjusted_(Y/N)'], inplace=True)
    #setting the order of the column names
    df_county_unemployment = df_county_unemployment[['Date_Id', 'Area_code', 'Labor_Force', 'Employment', 'Unemployment', 'Unemployment_Rate']]

    return {"area_code_dim":df_area_code.to_dict(orient="dict"),
        "unemployment_fact":df_county_unemployment.to_dict(orient="dict")}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
