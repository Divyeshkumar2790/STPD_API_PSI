import csv
import numpy as np
from matplotlib import pyplot as plt
import os
from datetime import datetime, timedelta
from STPD import STPD
from TPTR import TPTR

def generate_dates(start_month, start_year, num_months):
    """Generate a list of dates in datetime format starting from given month/year for num_months."""
    return [datetime(start_year + (start_month + i - 1) // 12, (start_month + i - 1) % 12 + 1, 1) for i in range(num_months)]

def convert_to_datetime(date_str, format="%m/%d/%Y"):
    """Convert a date string to a datetime object safely."""
    try:
        return datetime.strptime(date_str, format)
    except ValueError:
        print(f"Error: Invalid date format for {date_str}. Expected {format}.")
        return None  # Handle invalid dates gracefully

def filter_api_dates(api_dates, api_values, deformation_dates, threshold_days=30):
    """Filter API dates to keep only those that are close to deformation dates."""
    filtered_api_dates = []
    filtered_api_values = []
    
    for api_date, api_value in zip(api_dates, api_values):
        # Find the closest deformation date
        closest_deformation_date = min(deformation_dates, key=lambda d: abs(d - api_date))
        
        # Check if the API date is within the threshold range
        if abs((closest_deformation_date - api_date).days) <= threshold_days:
            filtered_api_dates.append(api_date)
            filtered_api_values.append(api_value)

    return filtered_api_dates, filtered_api_values

if __name__ == "__main__":
    # File paths
    csvpath = "D:/PhD_Main/STPD/STPD/LSWAVE-SignalProcessing/STPD_PythonPackage_EGhaderpour/DESC_CLIP.csv"
    apipath = "D:/PhD_Main/STPD/STPD/Output_API_mean.csv"

    # Ensure file existence
    if not os.path.exists(csvpath):
        print(f"Error: File {csvpath} not found.")
        exit()
    if not os.path.exists(apipath):
        print(f"Error: File {apipath} not found.")
        exit()

    # User-specified ID for plotting
    specific_id = input("Enter the ID you want to plot: ").strip()
    
    # Read time series data
    ids, latitudes, longitudes, times, series_values = [], [], [], [], []
    try:
        with open(csvpath, 'r') as csvfile:
            reader = csv.reader(csvfile, skipinitialspace=True)
            headers = next(reader)
            time_headers = headers[3:]
            times = [float(time) for time in time_headers]  # Ensure float conversion
            for row in reader:
                ids.append(row[0])
                latitudes.append(float(row[1]))
                longitudes.append(float(row[2]))
                series_values.append([float(val) if val else np.nan for val in row[3:]])
    except Exception as e:
        print(f"Error reading {csvpath}: {e}")
        exit()

    # Read API data
    api_dates, api_values = [], []
    try:
        with open(apipath, 'r') as api_file:
            api_reader = csv.reader(api_file, skipinitialspace=True)
            next(api_reader)  # Skip header
            for row in api_reader:
                date = convert_to_datetime(row[0], "%m/%d/%Y")
                if date:
                    api_dates.append(date)
                    api_values.append(float(row[1]))
    except Exception as e:
        print(f"Error reading {apipath}: {e}")
        exit()

    # Convert lists to numpy arrays
    series_values = np.array(series_values)
    deformation_dates = generate_dates(start_month=5, start_year=2011, num_months=len(times))

    # **Filter API dates that are not close to deformation dates**
    api_dates, api_values = filter_api_dates(api_dates, api_values, deformation_dates)

    # Print deformation time series dates
    print("Deformation Time Series Dates:")
    for date in deformation_dates:
        print(date.strftime("%Y-%m-%d"))

    # Process the specified ID
    id_found = False
    for i, (id_, lat, lon, f) in enumerate(zip(ids, latitudes, longitudes, series_values)):
        if id_ != specific_id:
            continue  # Skip IDs that do not match the specific ID
        
        id_found = True
        f = np.array(f)

        # Apply STPD to detect turning points in deformation time series
        TPs = STPD(times, f, size=60, step=12, SNR=1, NDRI=0.3, dir_th=0, tp_th=1, margin=12, alpha=0.01)
        if len(TPs) > 0:
            stats, y = TPTR(times, f, TPs)  # Obtain the overall trend `y`

            # Plot the time series with API data
            fig, ax1 = plt.subplots()

            # Primary y-axis: Deformation Time Series
            ax1.plot(deformation_dates, f, '-ok', label='Time Series', linewidth=1, markersize=3)
            ax1.plot(deformation_dates, y, 'b-', label='Linear Trend', linewidth=1)

            # Highlight turning points in blue
            turning_dates = [deformation_dates[int(tp)] for tp in TPs]
            turning_values = [f[int(tp)] for tp in TPs]
            ax1.plot(turning_dates, turning_values, 'ob', label='Turning Points')

            # Annotate turning points
            #for idx, tp in enumerate(TPs):
                #C = f"DIR={np.round(stats[idx][2], 2)}\n|NDRI|={np.round(stats[idx][4], 2)}"
                #ax1.text(deformation_dates[int(tp)], f[int(tp)], C, fontsize=8, bbox=dict(facecolor='yellow', alpha=0.5))

            # Annotate turning points with improved formatting and arrows
            for idx, tp in enumerate(TPs):
                annotation_text = f"$DIR$ = {np.round(stats[idx][2], 2)}\n$|NDRI|$ = {np.round(stats[idx][4], 2)}"
                ax1.annotate(annotation_text,
                 xy=(deformation_dates[int(tp)], f[int(tp)]),  # Turning point location
                 xytext=(deformation_dates[int(tp)], f[int(tp)] + 2),  # Offset for better visibility
                 fontsize=10, 
                 ha="center", 
                 bbox=dict(facecolor='yellow', edgecolor='black', boxstyle="round,pad=0.3", alpha=0.7),  # Improved box style
                 arrowprops=dict(arrowstyle="->", color="black", lw=1))  # Arrow pointing to turning point

            ax1.set_xlabel('Time')
            ax1.set_ylabel('Displacement (mm)', color='k')
            ax1.tick_params(axis='y', labelcolor='k')

            # Secondary y-axis: Filtered API Data
            ax2 = ax1.twinx()
            ax2.bar(api_dates, api_values, color='r', alpha=0.5, label='Filtered API Data', width=20)
            ax2.axhline(y=80, color='red', linestyle='--', linewidth=1.5, label='API Threshold (80 mm)')
            ax2.set_ylabel('API Value (mm)', color='r')
            ax2.tick_params(axis='y', labelcolor='r')

            # Title and legend
            fig.suptitle(f'Time Series and API Analysis for ID: {id_}')
            fig.legend(loc='upper left')

            # Format x-axis for datetime
            fig.autofmt_xdate()

            # Show and save plot
            fig.set_size_inches(12, 6)
            plt.grid(True)
            plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], ['2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022'])
            # Define save path
            save_path = f"D:/PhD_Main/STPD/STPD/LSWAVE-SignalProcessing/STPD_PythonPackage_EGhaderpour/FINAL/DESCENDING/PLOT/Time_Series_API_Analysis_{id_}.png"

            # Save the figure in high resolution
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved successfully at: {save_path}")
            plt.show()
            break  # Stop after processing the specific ID
    
    if not id_found:
        print(f"Error: ID '{specific_id}' not found in the dataset.")
