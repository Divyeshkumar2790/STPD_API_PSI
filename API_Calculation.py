import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import os

# Define file paths
input_file_path = os.path.join("D:", "PhD_Main", "STPD", "STPD", "Pdata_Petacciato.txt")
output_file_path = os.path.join("D:", "PhD_Main", "STPD", "STPD", "Output_API_mean.csv")

# Load the dataset
data = pd.read_csv(input_file_path, sep='\s+', header=None, names=['Date', 'Precipitation'])

# Convert 'Date' to datetime and 'Precipitation' to numeric
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y', errors='coerce')
data['Precipitation'] = pd.to_numeric(data['Precipitation'], errors='coerce')

# Drop rows with NaT or NaN values
data = data.dropna().sort_values('Date').reset_index(drop=True)

# Subset data from 2011 to 2022
data = data[(data['Date'] >= '2011-01-01') & (data['Date'] <= '2022-12-31')]

# Define decay factor
k = 0.85  # Adjust as needed

# Initialize API calculation
data['API'] = 0.0
for i in range(1, len(data)):
    data.iloc[i, data.columns.get_loc('API')] = (
        data.iloc[i, data.columns.get_loc('Precipitation')] + k * data.iloc[i-1, data.columns.get_loc('API')]
    )

# Define threshold for high API values
threshold = 100  # Adjust as needed

data['High_API'] = data['API'] > threshold

# Compute monthly mean API
data_monthly = data.resample('M', on='Date')['API'].mean().reset_index()

# Export monthly mean API data to CSV
data_monthly.to_csv(output_file_path, index=False)
print(f"API monthly average data exported to {output_file_path}")

# Plot the API values
plt.figure(figsize=(16, 10))
sc = plt.scatter(
    data['Date'], data['API'], c=data['API'], cmap='coolwarm', edgecolor='k', alpha=0.7, s=80
)

# Add color bar
cbar = plt.colorbar(sc)
cbar.set_label('API Level (mm)', fontsize=14)

# Highlight threshold line
plt.axhline(y=threshold, color='red', linestyle='--', linewidth=1.5, label=f'Threshold = {threshold} mm')

# Shade regions with high API
plt.fill_between(data['Date'], threshold, data['API'], where=(data['API'] > threshold), color='red', alpha=0.2, label='High API Spells')

# Format plot
plt.title('Enhanced API Spells Plot', fontsize=18)
plt.xlabel('Date', fontsize=14)
plt.ylabel('API (mm)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper left')

# Format x-axis with month/year ticks
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
