CREATE OR REPLACE TABLE crime-analysis-399301.crime_us_dataengineering.crime_tbl_analystics AS (
select f.Id,
       f.Incident_Id,
       f.Incident_Number, 
       dti.Date as Incident_Date,
       dti.Dayofmonth as Incident_Dayofmonth,
       dti.Month_Number as Incident_Month_Number,
       dti.Month_Name as Incident_Month_Name,
       dti.Dayofweek_number as Incident_Dayofweek_number, 
       dti.Dayofweek_name as Incident_Dayofweek_name, 
       dti.Year as Incident_Year,
       ti.Time as Incident_Time,
       ti.Hour as Incident_Hour,
       ti.Minute as Incident_Minute,
       dpti.Day_part as Incident_day_part,
       dtr.Date as Report_Date,
       dtr.Dayofmonth as Report_Dayofmonth,
       dtr.Month_Number as Report_Month_Number,
       dtr.Month_Name as Report_Month_Name,
       dtr.Dayofweek_number as Report_Dayofweek_number, 
       dtr.Dayofweek_name as Report_Dayofweek_name, 
       dtr.Year as Report_Year,
       tr.Time as Report_time, 
       tr.Hour as Report_Hour,
       tr.Minute as Report_minute,
       dptr.day_part as Report_day_part,
       inc.Incident_Code,
       inc.Incident_Category,
       inc.Incident_Subcategory,
       inc.Incident_Description,
       f.Report_Type_Code,
       rec.Report_Type_Description,
       f.Filed_Online,
       pd.Police_District,
       res.Resolution,
       loc.Latitude,loc.Longitude,loc.Point,
       nbh.Neighborhood,
       itr.Intersection
from crime-analysis-399301.crime_us_dataengineering.crime_incidents_fact_table as f
JOIN crime-analysis-399301.crime_us_dataengineering.date_dim as dti
ON f.Incident_Date_Id = dti.Id
JOIN crime-analysis-399301.crime_us_dataengineering.time_dim as ti
On f.Incident_Time_Id = ti.Id
JOIN crime-analysis-399301.crime_us_dataengineering.day_part_dim as dpti
On ti.Day_part_Id = dpti.Id
JOIN crime-analysis-399301.crime_us_dataengineering.date_dim as dtr
ON f.Report_Date_Id = dtr.Id
JOIN crime-analysis-399301.crime_us_dataengineering.time_dim as tr
On f.Report_Time_Id = tr.Id
JOIN crime-analysis-399301.crime_us_dataengineering.day_part_dim as dptr
On tr.Day_part_Id = dptr.Id
JOIN crime-analysis-399301.crime_us_dataengineering.incident_info_dim as inc
ON f.Incident_Code = inc.Incident_Code
JOIN crime-analysis-399301.crime_us_dataengineering.report_info_dim as rec
ON f.Report_Type_Code = rec.Report_Type_Code
JOIN crime-analysis-399301.crime_us_dataengineering.police_district_dim as pd
ON f.Police_district_Id = pd.Id
JOIN crime-analysis-399301.crime_us_dataengineering.resolution_dim as res
On f.Resolution_Id = res.Id
JOIN crime-analysis-399301.crime_us_dataengineering.location_dim as loc
ON f.Location_Id = loc.Id
JOIN crime-analysis-399301.crime_us_dataengineering.neighborhood_dim as nbh
ON f.Neighborhood_Id = nbh.Id
JOIN crime-analysis-399301.crime_us_dataengineering.intersection_dim as itr
ON f.Intersection_Id = itr.Id
ORDER BY f.Id ASC)
;
