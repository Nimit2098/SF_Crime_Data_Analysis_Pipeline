CREATE OR REPLACE TABLE crime-analysis-399301.crime_us_dataengineering.weather_tbl_analystics AS (
select wf.date_Id as Id,
       dt.Date,
       dt.Dayofmonth,
       dt.Month_Number,
       dt.Month_Name,
       dt.Dayofweek_number,
       dt.Dayofweek_name,
       dt.Year,
       wf.Temperature_Celcious,
       wf.Dew_Frost_Celcious,
       wf.Precipitation_mm_per_day,
       wf.Relative_Humidity_Percentagte,
       wf.Specific_Humidity_g_per_kg,
       wf.Wind_Speed_m_per_s       
from crime-analysis-399301.crime_us_dataengineering.weather_fact as wf
JOIN crime-analysis-399301.crime_us_dataengineering.date_dim as dt
ON wf.Date_Id = dt.Id
ORDER BY wf.date_Id ASC)
;