import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set global font size for research-quality plots
plt.rcParams.update({
    'font.size': 14,        # General font size
    'axes.titlesize': 16,   # Title font size
    'axes.labelsize': 14,   # Label font size
    'xtick.labelsize': 12,  # X-axis tick font size
    'ytick.labelsize': 12,  # Y-axis tick font size
    'legend.fontsize': 12,  # Legend font size
})

# Load the text file for pdata
file_path = r"D:\PhD_Main\STPD\STPD\Pdata_Petacciato.txt"
pdata = pd.read_csv(file_path, sep=r'\s+', header=None, names=['Date', 'Precipitation'])

# Load GPM monthly precipitation data
gpm = pd.read_csv(r"D:\PhD_Main\STPD\STPD\GPM.csv", header=None, names=['date', 'mean_precipitation'])

# Convert 'Date' to datetime and 'Precipitation' to numeric for pdata
pdata['Date'] = pd.to_datetime(pdata['Date'], format='%d/%m/%Y', errors='coerce')
pdata['Precipitation'] = pd.to_numeric(pdata['Precipitation'], errors='coerce')

# Convert 'date' to datetime and 'mean_precipitation' to numeric for gpm
gpm['date'] = pd.to_datetime(gpm['date'], errors='coerce')
gpm['mean_precipitation'] = pd.to_numeric(gpm['mean_precipitation'], errors='coerce')

# Subset pdata to the range from 2011 to 2022
pdata = pdata[(pdata['Date'] >= '2011-01-01') & (pdata['Date'] <= '2022-12-31')]

# Set 'Date' as the index for resampling
pdata.set_index('Date', inplace=True)

# Resample pdata to monthly frequency
monthly_data = pdata.resample('MS').mean()

# Align both dataframes by the date for correlation
gpm.set_index('date', inplace=True)

# Merge the two dataframes based on the index (date)
merged_data = monthly_data.join(gpm, how='inner')

# Drop NaN values before correlation calculation
merged_data.dropna(inplace=True)

# Calculate the Pearson correlation
correlation = merged_data['Precipitation'].corr(merged_data['mean_precipitation'])

# Scatter Plot with Regression Line
plt.figure(figsize=(9, 7))
sns.regplot(x='Precipitation', y='mean_precipitation', data=merged_data,
            scatter_kws={'s': 70, 'alpha': 0.7, 'color': 'blue'}, 
            line_kws={'color': 'red', 'linewidth': 2})

plt.title("Local Precipitation vs. GPM Precipitation", fontweight='bold')
plt.xlabel("Local Station Precipitation (mm)", fontweight='bold')
plt.ylabel("GPM Precipitation (mm)", fontweight='bold')

# Annotate the Pearson correlation on the plot
plt.text(0.05, 0.93, f'Pearson Correlation: {correlation:.2f}', 
         transform=plt.gca().transAxes, fontsize=14, color='black', 
         bbox=dict(facecolor='white', alpha=0.6, edgecolor='black'))

plt.grid(True, linestyle="--", alpha=0.6)
save_path = "D:/PhD_Main/STPD/STPD/RESULTS/Paper/Precipitation_Corr.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.show()

# Correlation Heatmap
correlation_matrix = merged_data[['Precipitation', 'mean_precipitation']].corr()

plt.figure(figsize=(7, 5))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=2,
            vmin=-1, vmax=1, cbar_kws={'label': 'Correlation Coefficient'}, 
            annot_kws={"size": 14, "fontweight": "bold"})

plt.title("Pearson Correlation Heatmap", fontweight='bold')
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')
save_path = "D:/PhD_Main/STPD/STPD/RESULTS/Paper/Heatmap.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.show()
