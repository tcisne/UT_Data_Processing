import os
import pandas as pd

# Global counters for naming
sample_num = 0  # Starting sample number (31 for the first file)
# Starting replicate number (1 for the first file)
replicate = 1  # This will be incremented for each file processed


# Function to process a single CSV file and save the result as an Excel file
def process_UT_data(file_path, output_folder):
    global sample_num, replicate  # Use global counters

    print(f"Processing file: {file_path}")  # Debugging statement

    # Step 1: Read the CSV file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Step 2: Extract Delta value (row 6, second value)
    delta_line = lines[5].strip()  # Row 6 is index 5
    delta = float(delta_line.split(",")[1])
    print(f"Delta: {delta} ")

    # Step 3: Load the amplitude data starting from row 31 (index 30)
    df = pd.read_csv(file_path, skiprows=30)

    # Check the number of columns
    print(f"Number of columns in {file_path}: {df.shape[1]}")  # Debugging statement

    # Step 4: Create a time column using the delta value
    df["Time"] = df.index * delta  # Assuming the index represents the sample number

    # Step 5: Select only the necessary columns (assuming first column is Amplitude)
    if df.shape[1] > 1:  # Ensure there is at least one amplitude column
        amplitude_data = df.iloc[:, [0]]  # Select only the first column (Amplitude)
        amplitude_data.columns = ["Amplitude"]  # Rename to Amplitude
    else:
        print(f"No amplitude data found in {file_path}.")  # Debugging statement
        return  # Exit if there's no amplitude data

    # Step 6: Create a new DataFrame with Time and Amplitude in the desired order
    result_df = pd.DataFrame(
        {
            "Time (us)": df["Time"],  # Time in column A
            "Amplitude (voltage)": amplitude_data["Amplitude"],  # Amplitude in column B
        }
    )

    # Step 7: Save the result to an Excel file in the output folder
    os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

    # Custom naming format: CB_<sample>.<replicate>.xlsx
    base_name = f"CB_{sample_num}.{replicate}"
    output_file = os.path.join(output_folder, base_name + ".xlsx")

    result_df.to_excel(output_file, index=False)  # Save without the index
    print(f"Processed data saved to: {output_file}")

    # Update replicate/sample count
    replicate += 1
    if replicate > 3:
        replicate = 1
        sample_num += 1


# Function to loop through all CSV files in a folder
def process_all_files(input_folder, output_folder):
    print(f"Looking for CSV files in folder: {input_folder}")  # Debugging statement
    # Loop through all CSV files in the folder
    for file_name in sorted(os.listdir(input_folder)):  # Ensure consistent order
        if file_name.lower().endswith(".csv"):  # Case-insensitive check for CSV files
            file_path = os.path.join(input_folder, file_name)
            process_UT_data(file_path, output_folder)
        else:
            print(
                f"Skipping non-CSV file: {file_name}"
            )  # Debugging statement for non-CSV files


# Example usage:
input_folder = r"C:\Users\tcisn\OneDrive - New Mexico State University\Research\Ultrasound cortical bone\UT_bone_test\CAL UT DATA"  # Ensure the correct folder path is specified
output_folder = r"C:\Users\tcisn\OneDrive - New Mexico State University\Research\Ultrasound cortical bone\UT_bone_test\CAL UT DATA"  # Set your specific output folder location

# Call the function to process all files in the folder
process_all_files(input_folder, output_folder)
