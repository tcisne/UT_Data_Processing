# Code to read ultrasound data (time vs amplitude) from excel sheets
# and perform analysis

# 1: Read in the reference sample data and specific sample data
# 2: Perform Hilber transform on both data sets to calculate the envelope
# 3: Find peak values of envelope signals
# 4: Determine the ToF by comparing ref and specific sample
# 5: Calcualte material properties

# STEP 1:
import pandas as pd
import os

# Read reference sample data
file_path_reference = r"C:\Users\tcisn\OneDrive - New Mexico State University\Research\Ultrasound cortical bone\UT_bone_test\CAL UT DATA\CAL2_225MHz.xlsx"
reference_data = pd.read_excel(
    file_path_reference, names=["Time_ref", "Amplitude_ref"], header=1
)

# Display reference sample columns to check
print("Reference Sample Data:")
print(reference_data.columns)

# Read sample dimensions and weights from a specific sheet
dimensions_file_path = r"C:\Users\tcisn\OneDrive - New Mexico State University\Research\Ultrasound cortical bone\UT_bone_test\Sample_data_original.xlsx"
dimensions_data = pd.read_excel(
    dimensions_file_path, sheet_name="All_Samples_Treated"
)  # Specify the sheet name here

# Create a list to store calculated sample data for each specific sample
sample_data_list = []

# Now, let's loop through all specific sample files in the folder
folder_path = r"C:\Users\tcisn\OneDrive - New Mexico State University\Research\Ultrasound cortical bone\UT_bone_test\All_Bovine_TREATED"
file_list = sorted(
    [f for f in os.listdir(folder_path) if f.endswith(".xlsx") and f.startswith("CB_")],
    key=lambda x: (
        int(x.split("_")[1].split(".")[0]),  # Sample number (e.g., 6, 7, 100)
        int(x.split("_")[1].split(".")[1]),  # Replicate number (1, 2, 3)
    ),
)

for file_name in file_list:
    # Extract sample name from file name
    file_path = os.path.join(folder_path, file_name)
    data_specific = pd.read_excel(file_path, names=["Time", "Amplitude"], header=1)
    time_specific = data_specific["Time"]
    amplitude_specific = data_specific["Amplitude"]

    # Display specific sample columns to check
    print("\nSpecific Sample Data -", file_name, ":")
    print(data_specific.columns)

    # STEP 2
    import numpy as np
    from scipy.signal import hilbert

    # Perform Hilbert transform to calculate envelope for reference
    reference_envelope = np.abs(hilbert(reference_data["Amplitude_ref"]))

    # Perform Hilbert transform to calculate evelope for specific sample
    specific_envelope = np.abs(hilbert(data_specific["Amplitude"]))

    # Verify the envelope was calcualted for each sample
    if specific_envelope is not None:
        print("Hilber transform calcualted successfully for", file_name)

        # STEP 3

        # Find peak values and corresponding times for each sample
        specific_peak_time_index = np.argmax(specific_envelope)
        specific_peak_time = data_specific["Time"].iloc[specific_peak_time_index]

        reference_peak_time_index = np.argmax(reference_envelope)
        reference_peak_time = reference_data["Time_ref"].iloc[reference_peak_time_index]

        # STEP 4

        # Calcualate time fo flight
        time_of_flight = abs(specific_peak_time - reference_peak_time) / 1e6
        print(f"Time of Flight: {time_of_flight} (s)")

        # Get dimensions and weight from the dimensions data DataFrame
        sample_name_full = os.path.splitext(file_name)[0]  # 'CB_1.1'
        sample_base = sample_name_full.split(".")[0]  # 'CB_1'

        matching_row = dimensions_data[dimensions_data["Sample"] == sample_base]

        if not matching_row.empty:
            sample_dimensions = matching_row.iloc[0]
        else:
            print(f"⚠️ No dimension entry found for {sample_base}, skipping...")
            continue  # Skip to the next sample

        # Chnage units from 'mm' & 'g' to 'm' and 'kg'
        thickness = sample_dimensions["Thickness (mm)"] / 1000
        length = sample_dimensions["Length (mm)"] / 1000
        width = sample_dimensions["Width (mm)"] / 1000
        weight = sample_dimensions["Weight (g)"] / 1000

        # STEP 5 Calculate material properties

        # Calculate density (rho)
        density_rho = weight / (thickness * length * width)
        print(f"Density: {density_rho} (kg/mm^3)")

        # Calculate wave velocity
        Wave_velocity = thickness / time_of_flight
        print(f"Wave Velocity: {Wave_velocity} (m/s)")

        # Calculate longitudinal elastic modulus
        Modulus_elast = (density_rho * Wave_velocity**2) / 1e9
        print(f"Longitudinal Elastic Modulus: {Modulus_elast} (GPa)")

        # Append sample calcuations to the list
        sample_data_list.append(
            {
                "Sample": file_name,
                "Time of Flight (s)": time_of_flight,
                "Density (kg/mm^3)": density_rho,
                "Wave velocity (m/s)": Wave_velocity,
                "Modulus (GPa)": Modulus_elast,
            }
        )

    else:
        print("Failed to calcualte Hilbert transform for", file_name)

    # Plot original and envelope signals

    # import matplotlib.pyplot as plt

    # plt.figure(figsize=(12,6))

    # # # Plot original reference sample signal
    # plt.subplot(2, 1, 1)
    # plt.plot(reference_data['Time_ref'], reference_data['Amplitude_ref'], label='Original Signal (Reference)')
    # plt.xlabel('Time (us)')
    # plt.ylabel('Amplitude (Voltage)')
    # plt.title('Reference Sample Ultrasound Signal')
    # plt.grid(True)

    # # # Plot envelope of reference sample signal
    # plt.plot(reference_data['Time_ref'], reference_envelope, label='Envelope')
    # plt.legend()

    # # Plot orignal specific sample signal
    # plt.subplot(2, 1, 2)
    # plt.plot(data_specific['Time'], data_specific['Amplitude'], label=[file_name])
    # plt.xlabel('Time (us)')
    # plt.ylabel('Amplitude (voltage)')
    # plt.title('Specific Sample Ultrasound Signal')
    # plt.grid(True)

    # # # Plot envelope of specific sample signal
    # plt.plot(data_specific['Time'], specific_envelope, label='Envelope')
    # plt.legend()

    # plt.tight_layout()
    # plt.show()

# Create a DataFrame from the list
sample_data = pd.DataFrame(sample_data_list)

# Save sample calculations to Excel file
sample_data.to_excel("Final_UT_Analysis_Results.xlsx", index=False)
