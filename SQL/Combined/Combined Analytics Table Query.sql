CREATE OR REPLACE TABLE crime-analysis-399301.crime_us_dataengineering.crime_weather_employment_tbl_analytics AS (
       SELECT CR.Id,
              CR.Incident_Id,
              CR.Incident_Number, 
              CR.Incident_Date,
              CR.Incident_Dayofmonth,
              CR.Incident_Month_Number,
              CR.Incident_Month_Name,
              CR.Incident_Dayofweek_number, 
              CR.Incident_Dayofweek_name, 
              CR.Incident_Year,
              CR.Incident_Time,
              CR.Incident_Hour,
              CR.Incident_Minute,
              CR.Incident_day_part,
              CR.Report_Date,
              CR.Report_Dayofmonth,
              CR.Report_Month_Number,
              CR.Report_Month_Name,
              CR.Report_Dayofweek_number, 
              CR.Report_Dayofweek_name, 
              CR.Report_Year,
              CR.Report_time, 
              CR.Report_Hour,
              CR.Report_minute,
              CR.Report_day_part,
              CR.Incident_Code,
              CR.Incident_Category,
              CR.Incident_Subcategory,
              CR.Incident_Description,
              CR.Report_Type_Code,
              CR.Report_Type_Description,
              CR.Filed_Online,
              CR.Police_District,
              CR.Resolution,
              CR.Latitude,
              CR.Longitude,
              CR.Point,
              CR.Neighborhood,
              CR.Intersection,
              WF.Temperature_Celcious,
              WF.Dew_Frost_Celcious,
              WF.Precipitation_mm_per_day,
              WF.Relative_Humidity_Percentagte,
              WF.Specific_Humidity_g_per_kg,
              WF.Wind_Speed_m_per_s,
              UE.Area_Name,
              UE.Labor_Force,
              UE.Employment,
              UE.Unemployment,
              UE.Unemployment_Rate
       FROM crime-analysis-399301.crime_us_dataengineering.crime_tbl_analystics as CR
       LEFT JOIN crime-analysis-399301.crime_us_dataengineering.weather_tbl_analystics as WF
       ON CR.Incident_Date = WF.Date
       LEFT JOIN crime-analysis-399301.crime_us_dataengineering.unemployment_tbl_analystics as UE
       ON CR.Incident_Month_Number = UE.Month_Number AND CR.Incident_Year = UE.Year
       WHERE UE.Area_Name = 'San Francisco County'
       ORDER BY CR.Id ASC)
  ;
