import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import matplotlib.patches as mpatches

# Read the results from the Excel file
results_file_path = r"D:\OneDrive - New Mexico State University\Research\Ultrasound cortical bone\Longitudinal Analysis Results_newWeight.xlsx"
data = pd.read_excel(results_file_path)

# Add group information (cow 1-4) based on the sampole index
conditions = [
    (data.index < 25),
    (data.index >= 25) & (data.index < 50),
    (data.index >= 50) & (data.index < 75),
    (data.index >= 75)
]
choices = ['Group 1', 'Group 2', 'Group 3', 'Group 4']
data['Group'] = np.select(conditions, choices)

# Display the first few rows of the data
print("Results Data:")
print(data.head())

# Perform basic statistical analysis
summary_stats = data.describe()
print("\nSummary Statistics:")
print(summary_stats)

# Calculate additional statistics if needed
mean_time_of_flight = data['Time of Flight (s)'].mean()
std_time_of_flight = data['Time of Flight (s)'].std()
print(f"\nMean Time of Flight: {mean_time_of_flight} s")
print(f"Standard Deviation of Time of Flight: {std_time_of_flight} s")

# Define a color paletter
palette = sns.color_palette('Set2', 4)
# Visualize the data
plt.figure(figsize=(16, 12))

# Histogram of Time of Flight
plt.subplot(2, 2, 1)
hist_plot = sns.histplot(data, x='Time of Flight (s)', hue='Group', kde=True, bins=20, palette=palette)
plt.title('Histogram of Time of Flight', fontsize=16)
plt.xlabel('Time of Flight (s)', fontsize=14)
plt.ylabel('Frequency', fontsize=14)

# Create a manual legend using patches
handles = [mpatches.Patch(color=palette[i], label=f'Group {i+1}') for i in range(len(choices))]
plt.legend(handles=handles, title='Group', fontsize=12)

# Boxplot of Density
plt.subplot(2, 2, 2)
sns.boxplot(x='Density (kg/mm^3)', y='Group', data=data, palette=palette)
plt.title('Boxplot of Density', fontsize=16)
plt.xlabel('Density (kg/mm^3)', fontsize=14)
plt.ylabel('Group', fontsize=14)
plt.grid(True)

# Scatter plot of Wave Velocity vs. Modulus with regression line
plt.subplot(2, 2, 3)
sns.scatterplot(x='Wave velocity (m/s)', y='Modulus (GPa)', hue='Group', data=data, palette=palette, s=100)
sns.regplot(x='Wave velocity (m/s)', y='Modulus (GPa)', data=data, scatter=False, color='blue')
plt.title('Scatter Plot of Wave Velocity vs. Modulus', fontsize=16)
plt.xlabel('Wave Velocity (m/s)', fontsize=14)
plt.ylabel('Modulus (GPa)', fontsize=14)
plt.legend(title='Group', fontsize=12)
plt.grid(True)

# Correlation heatmap
plt.subplot(2, 2, 4)
# Exclude the 'Sample' column for correlation colculation
corr_matrix = data.drop(columns=['Sample', 'Group']).corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, annot_kws={"size": 10})
plt.title('Correlation Heatmap', fontsize=16)

plt.tight_layout()
plt.show()

# Perform a correlation analysis
correlations = data.drop(columns=['Sample', 'Group']).corr()
print("\nCorrelation Matrix:")
print(correlations)

# Perform hypothesis testing (example: t-test for Time of Flight)
# Assuming you have a theoretical mean value to compare against
theoretical_mean_tof = 0.00000150  # Example value in seconds
t_stat, p_value = stats.ttest_1samp(data['Time of Flight (s)'], theoretical_mean_tof)
print(f"\nT-test for Time of Flight against a theoretical mean of {theoretical_mean_tof} s:")
print(f"T-statistic: {t_stat}")
print(f"P-value: {p_value}")

# Additional statistical tests can be performed as needed

# Save the summary statistics and correlations to an Excel file
output_file_path = "Processed_Results_newWeight.xlsx"
with pd.ExcelWriter(output_file_path) as writer:
    summary_stats.to_excel(writer, sheet_name='Summary Statistics')
    correlations.to_excel(writer, sheet_name='Correlations')

print(f"\nSummary statistics and correlation matrix saved to {output_file_path}")