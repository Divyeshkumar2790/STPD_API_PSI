# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:35:50 2024

@author: divye
"""
import geopandas as gpd
import pandas as pd

# Load the shapefile
shapefile_path = "D:\PhD_Main\STPD\STPD\Format_Datasets\Clip_Data\ASC_CLIP.shp"
gdf = gpd.read_file(shapefile_path)

# Extract columns starting with 'D' (time series data)
time_series_cols = [col for col in gdf.columns if col.startswith('D')]
time_series_df = gdf[time_series_cols].transpose()

# Convert column names to datetime if needed
time_series_df.index = pd.to_datetime(time_series_df.index, format='D%Y%m%d')

# Resample to monthly scale, taking the mean for each month
monthly_resampled = time_series_df.resample('M').mean().transpose()

# Calculate decimal year starting from zero
first_date = monthly_resampled.columns[0]
decimal_years = monthly_resampled.columns.to_series().apply(
    lambda date: (date.year - first_date.year) + (date.month - first_date.month) / 12
)
monthly_resampled.columns = decimal_years

# Combine resampled time series back with original non-time-series columns
gdf_resampled = gdf.drop(columns=time_series_cols)
gdf_resampled = pd.concat([gdf_resampled, monthly_resampled], axis=1)

# Save to a new CSV
output_csv = "D:\PhD_Main\STPD\STPD\Format_Datasets\Clip_Data\ASC_CLIP.csv"
gdf_resampled.to_csv(output_csv, index=False)

print(f"Time series resampled to monthly scale with decimal years starting from zero and saved to {output_csv}")
