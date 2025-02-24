import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
file_path = r"D:\PhD_Main\STPD\STPD\LSWAVE-SignalProcessing\STPD_PythonPackage_EGhaderpour\DESC_ALL_CLIP\DESC_filtered_turning_points.csv"
df = pd.read_csv(file_path)

# Define bins similar to the image
bins = [-np.inf, -10, -8, -6, -4, -2, 2, 4, 6, 8, 10, np.inf]
bin_labels = ["< -10", "[-10 -8)", "[-8 -6)", "[-6 -4)", "[-4 -2)", "[-2 2)",
              "[2 4)", "[4 6)", "[6 8)", "[8 10)", "> 10"]

# Categorize the 'Direction' values into bins
df["Direction_Bin"] = pd.cut(df["Direction"], bins=bins, labels=bin_labels, right=False)

# Count occurrences per bin
bin_counts = df["Direction_Bin"].value_counts().reindex(bin_labels, fill_value=0)

# Separate counts for positive and negative slopes
positive_counts = df[df["Slope"] >= 0]["Direction_Bin"].value_counts().reindex(bin_labels, fill_value=0)
negative_counts = df[df["Slope"] < 0]["Direction_Bin"].value_counts().reindex(bin_labels, fill_value=0)

# Define font sizes for a research-quality figure
TITLE_SIZE = 18
LABEL_SIZE = 14
TICK_SIZE = 12
LEGEND_SIZE = 14

# Plot the bar chart
fig, ax = plt.subplots(figsize=(10, 5))
bar_width = 0.4
x = np.arange(len(bin_labels))

ax.bar(x - bar_width/2, negative_counts, bar_width, color='red', label='Negative Slopes')
ax.bar(x + bar_width/2, positive_counts, bar_width, color='blue', label='Positive Slopes')

# Formatting
ax.set_xticks(x)
ax.set_xticklabels(bin_labels, rotation=45, ha="right")
ax.set_xlabel("Direction of Turning Points (mm/year)")
ax.set_ylabel("Turning Point Frequency")
ax.set_title("Turning Point Frequency by Direction - Descending")
ax.legend()

# Show plot
plt.tight_layout()
# Save a high-quality figure for publication
plt.savefig("D:/PhD_Main/STPD/STPD/RESULTS/Paper/TPF_DESCENDING_HighRes.png", dpi=300, bbox_inches='tight')
plt.show()
