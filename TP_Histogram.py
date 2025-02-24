import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# File paths
desc_file = r"D:\PhD_Main\STPD\STPD\LSWAVE-SignalProcessing\STPD_PythonPackage_EGhaderpour\DESC_ALL_CLIP\DESC_filtered_turning_points.csv"
asc_file = r"D:\PhD_Main\STPD\STPD\LSWAVE-SignalProcessing\STPD_PythonPackage_EGhaderpour\ASC_ALL_CLIP\ASC_filtered_turning_points.csv"

# Load datasets
df_desc = pd.read_csv(desc_file)
df_asc = pd.read_csv(asc_file)

def parse_dates(date_series):
    """Convert dates from different formats to YYYY-MM."""
    date_series = date_series.astype(str).str.strip()  # Remove spaces
    
    formats = ['%y-%b', '%b-%y']  # Correct formats for each dataset

    parsed_dates = None
    for fmt in formats:
        try:
            parsed_dates = pd.to_datetime(date_series, errors='coerce', format=fmt)
            if parsed_dates.notna().sum() > 0:
                print(f"Using format {fmt} for parsing.")  # Debugging output
                break  # Stop when a valid format is found
        except Exception as e:
            continue  # Skip errors

    if parsed_dates is None:
        raise ValueError("No valid date format found!")

    # Fix incorrect century (assuming data is from 2000s, not 1900s)
    parsed_dates = parsed_dates.apply(lambda x: x.replace(year=x.year + 100) if pd.notnull(x) and x.year < 2000 else x)

    # Convert to Period format for grouping
    return parsed_dates.dt.to_period('M')


# Debugging: Check if missing values are fixed
print("Missing Dates in Descending Orbit Data:", df_desc['Date (mm/yyyy)'].isna().sum())
print("Missing Dates in Ascending Orbit Data:", df_asc['Date (mm/yyyy)'].isna().sum())


# Example usage:
df_desc['Date (mm/yyyy)'] = parse_dates(df_desc['Date (mm/yyyy)'])
df_asc['Date (mm/yyyy)'] = parse_dates(df_asc['Date (mm/yyyy)'])

# Debugging step: Check for missing dates
print("Missing Dates in Descending Orbit Data:", df_desc['Date (mm/yyyy)'].isna().sum())
print("Missing Dates in Ascending Orbit Data:", df_asc['Date (mm/yyyy)'].isna().sum())

# Remove rows with NaT values in date column
df_desc = df_desc.dropna(subset=['Date (mm/yyyy)'])
df_asc = df_asc.dropna(subset=['Date (mm/yyyy)'])

# Count turning points per date for each orbit
hist_desc = df_desc.groupby('Date (mm/yyyy)')['ID'].count().rename("Descending Orbit")
hist_asc = df_asc.groupby('Date (mm/yyyy)')['ID'].count().rename("Ascending Orbit")

# Debugging step: Check if data is correctly grouped
print("Descending Orbit Data:\n", hist_desc.head(10))
print("Ascending Orbit Data:\n", hist_asc.head(10))

# Merge datasets and fill missing values with 0
hist_combined = pd.concat([hist_desc, hist_asc], axis=1).fillna(0)

# Convert Period index to datetime for plotting
hist_combined.index = hist_combined.index.to_timestamp()

max_desc_month = hist_combined["Descending Orbit"].idxmax()
max_desc_value = hist_combined["Descending Orbit"].max()

max_asc_month = hist_combined["Ascending Orbit"].idxmax()
max_asc_value = hist_combined["Ascending Orbit"].max()

max_total_month = hist_combined.sum(axis=1).idxmax()
max_total_value = hist_combined.sum(axis=1).max()

print(f"Maximum Descending Orbit Turning Points: {max_desc_value} in {max_desc_month.strftime('%b-%Y')}")
print(f"Maximum Ascending Orbit Turning Points: {max_asc_value} in {max_asc_month.strftime('%b-%Y')}")
print(f"Overall Maximum Turning Points: {max_total_value} in {max_total_month.strftime('%b-%Y')}")


# Define font sizes for a research-quality figure
TITLE_SIZE = 18
LABEL_SIZE = 14
TICK_SIZE = 12
LEGEND_SIZE = 14

plt.figure(figsize=(14, 7))  # Larger figure for better readability

# Plot both datasets
bar_width = 25  # Slightly increased bar width
plt.bar(hist_combined.index, hist_combined["Ascending Orbit"], width=bar_width, 
        label="Ascending Orbit", alpha=0.8, color="darkorange", edgecolor="black", linewidth=1.2, 
        bottom=hist_combined["Descending Orbit"])

plt.bar(hist_combined.index, hist_combined["Descending Orbit"], width=bar_width, 
        label="Descending Orbit", alpha=0.8, color="steelblue", edgecolor="black", linewidth=1.2)

# Formatting with improved font sizes
plt.xlabel("Date", fontsize=LABEL_SIZE, fontweight='bold')
plt.ylabel("Turning Point Frequency", fontsize=LABEL_SIZE, fontweight='bold')
plt.title("Histogram of Turning Points Over Time\n(Ascending & Descending Orbits)", fontsize=TITLE_SIZE, fontweight='bold')

plt.xticks(rotation=45, fontsize=TICK_SIZE)
plt.yticks(fontsize=TICK_SIZE)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))

# Grid and legend improvements
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.legend(fontsize=LEGEND_SIZE, loc="upper left", frameon=True)

plt.tight_layout()

# Save a high-quality figure for publication
plt.savefig("D:/PhD_Main/STPD/STPD/Combined_Histogram_HighRes.png", dpi=600, bbox_inches='tight')

# Show the plot
plt.show()