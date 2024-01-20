CREATE OR REPLACE TABLE crime-analysis-399301.crime_us_dataengineering.unemployment_tbl_analystics AS (
select unef.date_Id as Id,
       dt.Date,
       dt.Dayofmonth,
       dt.Month_Number,
       dt.Month_Name,
       dt.Dayofweek_number,
       dt.Dayofweek_name,
       dt.Year,
       ac.Area_Name,
       unef.Labor_Force,
       unef.Employment,
       unef.Unemployment,
       unef.Unemployment_Rate
from crime-analysis-399301.crime_us_dataengineering.unemployment_fact as unef
JOIN crime-analysis-399301.crime_us_dataengineering.area_code_dim as ac
ON unef.Area_code = ac.Area_code
JOIN crime-analysis-399301.crime_us_dataengineering.date_dim as dt
ON unef.Date_Id = dt.Id
ORDER BY unef.date_Id ASC)
;