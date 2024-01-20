import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df_weather, *args, **kwargs):
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
    #Init of a dict for day part
    day_part_dict = {1: 'Late Night', 2: 'Early Morning', 3: 'Morning', 4: 'Noon', 5: 'Evening', 6: 'Night'}
    #Converting dict to dataframe
    df_day_part = pd.DataFrame(list(day_part_dict.items()), columns=['Id', 'day_part'])

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

    #Init of a dataframe for the time dimension table
    df_time = pd.DataFrame(pd.date_range(start="2000-01-01", end="2000-01-02", freq="T", inclusive='left'))
    df_time['Id'] = df_time.index
    #To extract various components from the time column
    #extract time from datetime column
    df_time['Time'] = df_time[0].dt.time
    #extract hour from datetime column
    df_time['Hour'] = df_time[0].dt.hour
    #extract minutes from datetime column
    df_time['Minute'] = df_time[0].dt.minute
    #calculate the categorical number from the hour column for the day part
    df_time['Day_part'] = (df_time['Hour'] % 24 + 4) // 4
    #mapping the day part name for the numerical value
    df_time['Day_part'] = df_time['Day_part'].replace(day_part_dict)
    #mapping the day part name from the dimension table of day part
    df_time['Day_part_Id'] = df_time['Day_part'].replace(df_day_part.set_index('day_part')['Id'])


    #dropping the unnecessary column
    df_time.drop(columns=[0, 'Day_part'], inplace=True)

    #delete the last incomplete entry from the dataset
    df_weather.drop(df_weather.index[-1], inplace=True)
    #concat date components to create a date column
    df_weather['Date'] = df_weather['YEAR'].astype(str) + '-' + df_weather['MO'].astype(str) + '-' + df_weather['DY'].astype(str)
    #convert the date column to datetime format
    df_weather['Date'] = pd.to_datetime(df_weather['Date'])
    #mapping the id(primary key) of dimension tables to the fact table
    df_weather['Date_Id'] = df_weather['Date'].map(df_date.set_index('Date')['Id'])
    #drop unnecessary columns
    df_weather.drop(columns=['YEAR', 'MO', 'DY', 'Date'], inplace=True)
    #set the order of the columns in dataframe
    df_weather = df_weather[['Date_Id', 'T2M', 'T2MDEW', 'PRECTOTCORR', 'RH2M', 'QV2M', 'WS10M']]
    # renaming the columns
    df_weather.columns = ['Date_Id', 'Temperature_Celcious', 'Dew_Frost_Celcious', 'Precipitation_mm_per_day', 'Relative_Humidity_Percentagte', 'Specific_Humidity_g_per_kg', 'Wind_Speed_m_per_s']

    return {"time_dim":df_time.to_dict(orient="dict"),
            "day_part_dim":df_day_part.to_dict(orient="dict"),
            "weather_fact":df_weather.to_dict(orient="dict")}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
