import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import scienceplots

plt.style.use(['science', 'notebook', 'grid'])

# Increase the `num_points` value for smoother curves
def smooth_curve (time, amplitude, num_points=1000):
    # Smooth the curve using interpolation
    num_points = 5000
    time_smooth = np.linspace(time.min(), time.max(), num_points)
    spl = make_interp_spline(time, amplitude, k=3)  # Cubic spline interpolation
    amplitude_smooth = spl(time_smooth)
    return time_smooth, amplitude_smooth

# Read data from main sample
file_path_main = r"F:\WAVE\Processed_UT_Data\SteelBlock_225MHz_processed.xlsx"
data_main = pd.read_excel(file_path_main, names=['Time (us)', 'Amplitude (voltage)'])

# Read data from reference sample
file_path_ref = r"F:\WAVE\Processed_UT_Data\Ref_225MHz_processed.xlsx"
data_ref = pd.read_excel(file_path_ref, names=['Time (us)', 'Amplitude (voltage)'])

# Assuming the Excel sheet has columns named 'Time' and 'Amplitude'
time_main = data_main['Time (us)']
amplitude_main = data_main['Amplitude (voltage)']

time_ref = data_ref['Time (us)']
amplitude_ref = data_ref['Amplitude (voltage)']

# Smooth curves for both datasets
time_smooth_main, amplitude_smooth_main = smooth_curve(time_main, amplitude_main)
time_smooth_ref, amplitude_smooth_ref = smooth_curve(time_ref, amplitude_ref)

# Plotting
#plt.figure(figsize=(10, 6))

#plt.plot(time_smooth_main, amplitude_smooth_main, label='Cortical bone', color='blue')
#plt.plot(time_smooth_ref, amplitude_smooth_ref, label='No sample', color='green')
#plt.scatter(time_main, amplitude_main, label='Original Data', color='red')
#plt.scatter(time_ref, amplitude_ref, label='Original Data', color='orange')

#plt.xlabel('Time ($\mu$s)', {'weight': 'bold', 'size': 12})
#plt.ylabel('Amplitude (V)', {'weight': 'bold', 'size': 12})
#plt.title('Thru-Transmission Ultrasound Signal Data', {'weight': 'bold', 'size': 12})
#plt.legend()
#plt.grid(True)
#plt.show()

fig, ax = plt.subplots(1, 1, figsize=(10,6))
ax.plot(time_smooth_main, amplitude_smooth_main,label='SteelBlock (1018)', color='red', linewidth=1 )
ax.plot(time_smooth_ref, amplitude_smooth_ref, label='No sample',color='blue', linewidth=1)
ax.legend(loc='upper right', fancybox=False, edgecolor='black', fontsize='9')
ax.set_title('Frequency: 2.25 MHz')
#ax.set_xlabel('Time [$\mu$s]')
ax.set_xlabel('Time [seconds]')
ax.set_ylabel('Amplitude [voltage]')
plt.show()