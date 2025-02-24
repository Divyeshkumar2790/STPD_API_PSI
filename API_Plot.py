import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# File path to your API dataset
apipath = "D:/PhD_Main/STPD/STPD/Output_API_mean.csv"

# Load the dataset
df = pd.read_csv(apipath)

# Ensure correct column names (Modify based on your dataset)
df.columns = ['Date', 'API']  # Assuming the second column contains API values

# Convert Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Sort data by date
df = df.sort_values(by='Date')

# Set the API threshold for high spells
api_threshold = 90  # Adjusted threshold to 60 mm

# Identify high API spells
df['High_Spell'] = df['API'] >= api_threshold  # Boolean column for high API spells

# Create the figure
plt.figure(figsize=(16, 7))

# Plot all API values as red bars
plt.bar(df['Date'], df['API'], color='lightcoral', width=10, alpha=0.7, edgecolor='black', label="API Values")

# Highlight bars above the threshold in dark red
plt.bar(df[df['High_Spell']]['Date'], df[df['High_Spell']]['API'], 
        color='darkred', width=10, edgecolor='black', alpha=0.9, label="High API Spells (≥ 90mm)")

# Add threshold line
plt.axhline(y=api_threshold, color='red', linestyle='dashed', linewidth=2, label=f'Threshold = {api_threshold} mm')

# Labels and title
plt.title("API Bar Plot with Highlighted High Spells", fontsize=18, fontweight='bold')
plt.xlabel("Date", fontsize=14, fontweight='bold')
plt.ylabel("API Value (mm)", fontsize=14, fontweight='bold')

# Improve aesthetics
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle="--", alpha=0.6)
plt.legend(fontsize=12)
plt.tight_layout()

# Show the plot
save_path = "D:/PhD_Main/STPD/STPD/RESULTS/Paper/API_PLOT.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.show()
