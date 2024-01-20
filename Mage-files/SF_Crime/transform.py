import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
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

    #Changing names of columns to insert Underscore in spaces
    df.rename(columns=lambda x: x.strip().replace(" ","_"),inplace=True)

    #standardizing the Report code respective to the report type description
    #Init of the dictionary
    Report_Code_correction = {
        'Vehicle Supplement' : 'VS',
        'Coplogic Initial' : 'CI',
        'Coplogic Supplement' : 'CS',
        'Initial' : 'II',
        'Initial Supplement' : 'IS',
        'Vehicle Initial': 'VI'
    }
    #mapping the standardized values using the dictionary to dataframe column values
    df['Report_Type_Code'] = df['Report_Type_Description'].map(Report_Code_correction)


    #to standardize the values in the Incident Category column that represent the same concept
    #Init of the dictionary
    replace_dict = {
        'Recovered Vehicle': 'Vehicle Theft and Recovery',
        'Motor Vehicle Theft': 'Vehicle Theft and Recovery',
        'Motor Vehicle Theft?': 'Vehicle Theft and Recovery',
        'Recovered Vehicle': 'Vehicle Theft and Recovery',
        'Larceny Theft': 'Property Crimes',
        'Lost Property': 'Property Crimes',
        'Stolen Property': 'Property Crimes',
        'Burglary': 'Property Crimes',
        'Vandalism': 'Property Crimes',
        'Drug Violation': 'Drug-related Incidents',
        'Drug Offense': 'Drug-related Incidents',
        'Non-Criminal': 'Miscellaneous',
        'Case Closure': 'Miscellaneous',
        'Other Miscellaneous': 'Miscellaneous',
        'Other Offenses': 'Miscellaneous',
        'Other': 'Miscellaneous',
        'Miscellaneous Investigation': 'Miscellaneous',
        'Suspicious Occ': 'Suspicious',
        'Suspicious': 'Suspicious',
        'Missing Person': 'Police Interaction Incidents',
        'Courtesy Report': 'Police Interaction Incidents',
        'Fraud': 'Fraudulent Activities',
        'Forgery And Counterfeiting': 'Fraudulent Activities',
        'Prostitution': 'Sex-related Incidents',
        'Human Trafficking, Commercial Sex Acts': 'Sex-related Incidents',
        'Human Trafficking (A), Commercial Sex Acts': 'Sex-related Incidents',
        'Human Trafficking (B), Involuntary Servitude': 'Sex-related Incidents',
        'Embezzlement': 'Financial and Regulatory Offenses',
        'Gambling': 'Financial and Regulatory Offenses',
        'Liquor Laws': 'Financial and Regulatory Offenses'
    }
    #mapping the standardized values using the dictionary to dataframe column values
    df['Incident_Category'].replace(replace_dict, inplace=True)


    #To fill the missing values in the Incident Category by using the respective Incident Description
    #Init of the dictionary
    description_to_incident = {
        'Vehicle, Seizure Order Service': 'Vehicle Theft and Recovery',
        'Gun Violence Restraining Order': 'Weapons Offense',
        'Driving, Stunt Vehicle/Street Racing': 'Traffic Collision',
        'Cryptocurrency Related Crime (secondary code only)': 'Financial and Regulatory Offenses',
        'Auto Impounded': 'Vehicle Impounded',
        'Theft, Boat': 'Property Crimes',
        'Theft, Animal, Att.': 'Property Crimes',
        'SFMTA Muni Transit Operator-Bus/LRV': 'SFMTA',
        'Military Ordinance': 'Weapons Offense',
        'SFMTA Parking and Control Officer': 'SFMTA',
        'Cloned Cellular Phone, Use': 'Fraudulent Activities',
        'Public Health Order Violation, Notification': 'Miscellaneous',
        'Public Health Order Violation, After Notification': 'Miscellaneous',
        'Assault, Commission of While Armed': 'Assault',
        'Theft, Phone Booth, <$50': 'Property Crimes',
        'Gun Violence Restraining Order Violation': 'Weapons Offense',
        'Theft, Phone Booth, $200-$950': 'Property Crimes',
        'Theft, Phone Booth, $50-$200': 'Property Crimes',
        'Vehicle, Seizure Order': 'Vehicle Theft and Recovery',
        'SFMTA Employee-Non Operator/Station Agent-Other Employee': 'SFMTA',
        'Assault, By Police Officers': 'Assault',
        'Crimes Involving Receipts or Titles': 'Fraudulent Activities',
        'Procurement, Pimping, & Pandering': 'Sex-related Incidents',
        'Service of Documents Related to a Civil Drug Abatement and/or Public Nuisance Action': 'Miscellaneous',
        'Pyrotechnic Explosive Device - Barrel Bomb': 'Fire Report',
        'Theft, Phone Booth, >$950': 'Property Crimes'
    }
    #mapping the standardized values using the dictionary to dataframe column values
    df['Incident_Category'] = df['Incident_Category'].fillna(df['Incident_Description'].map(description_to_incident))


    #converting date columns to datetime format in dataframe
    df['Incident_Datetime']= pd.to_datetime(df['Incident_Datetime'], format= '%Y/%m/%d %I:%M:%S %p')
    df['Report_Datetime']= pd.to_datetime(df['Report_Datetime'], format= '%Y/%m/%d %I:%M:%S %p')

    #dropping the incomplete month data of September 2023
    #df = df.drop((df[(df['Incident_Datetime'].dt.month == 9) & (df['Incident_Year'] == 2023)]).index)

    #Converting boolean column to binary column
    df['Filed_Online'] = df['Filed_Online'].notnull().astype(int)

    df = df[(df['Incident_Datetime'] <= '2023-12-31 23:59:59') & (df['Report_Datetime'] <= '2023-12-31 23:59:59')]

    #Init of a dict for day part
    day_part_dict = {1: 'Late Night', 2: 'Early Morning', 3: 'Morning', 4: 'Noon', 5: 'Evening', 6: 'Night'}
    #Converting dict to dataframe
    df_day_part = pd.DataFrame(list(day_part_dict.items()), columns=['Id', 'day_part'])

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

    #Init of a dataframe for the dimension table
    df_date = pd.DataFrame(pd.date_range(start='2018-01-01 00:01:00', end='2023-12-31 23:59:59', freq="D", inclusive='both'))
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

    #Init of a function
    #To transform the tables into new dataframe for dimension tables
    def dimension_tbl_fun(df_temp):
        #dropping the duplicate rows across the dataframe
        df_temp.drop_duplicates(inplace=True)
        #dropping missing values
        df_temp.dropna(inplace=True)
        #Resetting the index after drop code
        df_temp.reset_index(inplace=True)
        #dropping unnecessary columns
        df_temp.drop(columns=['index'], inplace=True)
        #creating a primary key column using index of the dataframe
        df_temp['Id'] = df_temp.index
        return df_temp

    #Calling the dimension functions
    df_report_info = dimension_tbl_fun(df[['Report_Type_Code','Report_Type_Description']].copy())
    #dropping unnecessary columns
    df_report_info.drop(columns='Id',inplace=True)

    #Init of a dataframe for the dimension table
    df_incident_info = df[['Incident_Code','Incident_Category','Incident_Subcategory','Incident_Description']].copy()
    #dropping the duplicate rows across the dataframe
    df_incident_info.drop_duplicates(inplace=True)
    #Dropping the row with duplicate incident code = 7060
    #df_incident_info.drop(labels=[283526], inplace=True)
    #Resetting the index after drop code
    df_incident_info.reset_index(inplace=True)
    #dropping unnecessary columns
    df_incident_info.drop(columns=['index'], inplace=True)

    #Calling the dimension functions
    df_police_district = dimension_tbl_fun(df[['Police_District']].copy())
    #setting the order of the columns in dataframe
    df_police_district = df_police_district[['Id', 'Police_District']]

    #Calling the dimension functions
    df_resolution = dimension_tbl_fun(df[['Resolution']].copy())
    #setting the order of the columns in dataframe
    df_resolution = df_resolution[['Id', 'Resolution']]

    #Calling the dimension functions
    df_neighborhood = dimension_tbl_fun(df[['Analysis_Neighborhood']].copy())
    #setting the order of the columns in dataframe
    df_neighborhood = df_neighborhood[['Id', 'Analysis_Neighborhood']]
    #renaming the column
    df_neighborhood.rename(columns={'Analysis_Neighborhood': 'Neighborhood'}, inplace=True)

    #Calling the dimension functions
    df_location = dimension_tbl_fun(df[['Latitude','Longitude','Point']].copy())
    #setting the order of the columns in dataframe
    df_location = df_location[['Id', 'Latitude', 'Longitude', 'Point']]

    #Calling the dimension functions
    df_intersection = dimension_tbl_fun(df[['Intersection']].copy())
    #setting the order of the columns in dataframe
    df_intersection = df_intersection[['Id', 'Intersection']]

    #Init of a dataframe for the Fact database table
    df_fact_table = df.copy()

    #mapping the id(primary key) of dimension tables to the fact table
    df_fact_table['Incident_Time_Id'] = df_fact_table['Incident_Datetime'].dt.time.map(df_time.set_index('Time')['Id'])
    df_fact_table['Incident_Date_Id'] = df_fact_table['Incident_Datetime'].dt.date.map(df_date.set_index('Date')['Id'])
    df_fact_table['Report_Time_Id'] = df_fact_table['Report_Datetime'].dt.time.map(df_time.set_index('Time')['Id'])
    df_fact_table['Report_Date_Id'] = df_fact_table['Report_Datetime'].dt.date.map(df_date.set_index('Date')['Id'])
    df_fact_table['Intersection_Id'] = df_fact_table['Intersection'].map(df_intersection.set_index('Intersection')['Id'])
    df_fact_table['Police_district_Id'] = df_fact_table['Police_District'].map(df_police_district.set_index('Police_District')['Id'])
    df_fact_table['Resolution_Id'] = df_fact_table['Resolution'].map(df_resolution.set_index('Resolution')['Id'])
    df_fact_table['Neighborhood_Id'] = df_fact_table['Analysis_Neighborhood'].map(df_neighborhood.set_index('Neighborhood')['Id'])
    #to merge fact and dimension table for the location to get id(primary key) to the fact table
    df_fact_table = df_fact_table.merge(df_location, on=['Latitude', 'Longitude', 'Point'], how='left')
    #renaming the column
    df_fact_table.rename(columns={'Id':'Location_Id'}, inplace=True)

    #dropping the unwanted columns
    df_fact_table.drop(columns=['CAD_Number', 'CNN', 'Invest_In_Neighborhoods_(IIN)_Areas', 'ESNCAG_-_Boundary_File', 'Central_Market/Tenderloin_Boundary_Polygon_-_Updated', 'Civic_Center_Harm_Reduction_Project_Boundary', 
                    'HSOC_Zones_as_of_2018-06-05', 'Supervisor_District', 'Supervisor_District_2012', 'Latitude', 'Latitude', 'Point', 'Row_ID', 'Incident_Datetime', 'Incident_Date', 'Incident_Time', 'Incident_Year',
                    'Incident_Day_of_Week', 'Report_Datetime', 'Report_Type_Description', 'Incident_Category', 'Incident_Subcategory', 'Incident_Description', 'Resolution','Intersection', 'Police_District', 'Analysis_Neighborhood',
                    'Longitude', 'Neighborhoods', 'Current_Supervisor_Districts', 'Current_Police_Districts'], inplace=True)

    #Dropping the NA values
    df_fact_table.dropna(inplace=True)

    #adding columns for the primary key
    df_fact_table.reset_index(inplace=True)
    df_fact_table.drop(columns=['index'], inplace=True)
    df_fact_table['Id'] = df_fact_table.index


    #to order the columns in fact database
    df_fact_table = df_fact_table[['Id', 'Incident_ID', 'Incident_Number', 'Incident_Date_Id', 'Incident_Time_Id', 'Report_Date_Id', 'Report_Time_Id', 'Incident_Code', 'Report_Type_Code', 'Filed_Online', 'Police_district_Id', 'Resolution_Id',
                                'Location_Id', 'Neighborhood_Id', 'Intersection_Id']]

    #converting the column id's to integer type|
    df_fact_table[['Location_Id', 'Neighborhood_Id', 'Intersection_Id']] = df_fact_table[['Location_Id', 'Neighborhood_Id', 'Intersection_Id']].astype(int)

    return {"date_dim":df_date.to_dict(orient="dict"),
        "time_dim":df_time.to_dict(orient="dict"),
        "report_info_dim":df_report_info.to_dict(orient="dict"),
        "location_dim":df_location.to_dict(orient="dict"),
        "intersection_dim":df_intersection.to_dict(orient="dict"),
        "neighborhood_dim":df_neighborhood.to_dict(orient="dict"),
        "resolution_dim":df_resolution.to_dict(orient="dict"),
        "police_district_dim":df_police_district.to_dict(orient="dict"),
        "incident_info_dim":df_incident_info.to_dict(orient="dict"),
        "day_part_dim":df_day_part.to_dict(orient="dict"),
        "crime_incidents_fact_table":df_fact_table.to_dict(orient="dict")}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
