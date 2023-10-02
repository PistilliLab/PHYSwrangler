import pandas as pd
import os

def read_data(file_path, sheet_name='Fatigue-AUC'):
    """
    Reads the data from the specified Excel file and sheet.
    """
    return pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')  # specify engine to open .xlsx

def average_every_10_measurements(df, subject_ids, groups):
    """
    Averages every 10 measurements for the specified subject IDs.
    Returns a dataframe with the results.
    """
    # Convert the 'EDL' column to string and strip any trailing spaces
    df['EDL'] = df['EDL'].astype(str).str.strip()

    # Convert the input subject IDs to string
    subject_ids = [str(sid).strip() for sid in subject_ids]

    # List to store the result dataframes for each subject
    result_dfs = []

    # Iterate over each subject ID in the input list
    for subject_id in subject_ids:
        # Locate the row corresponding to the subject ID
        data_row = df[df['EDL'] == subject_id]

        # If the subject ID is found in the dataframe
        if not data_row.empty:
            # Extract the data (excluding the subject ID column)
            values = data_row.iloc[0, 1:].values

            # Compute the average for every 10 measurements
            averaged_values = [values[i:i+10].mean() for i in range(0, len(values), 10)]

            # Create a dataframe for the subject
            subject_df = pd.DataFrame({
                "Subject_ID": [subject_id],
                "Group": [groups[subject_id]],
                **{str((i+1)*10): [averaged_values[i]] for i in range(len(averaged_values))}
            })

            result_dfs.append(subject_df)

    # Concatenate all the subject dataframes
    result_df = pd.concat(result_dfs, ignore_index=True)

    return result_df

if __name__ == "__main__":
    # Path to the Excel file
    file_path = "/path/to/file.xlsx"

    # List of subject IDs you want to process
    subject_ids_list = ["2362", "2365", "2367", "2370", "2372", "2361", "2363", "2364", "2366", "2368", "2371"]

    # Define the group for each subject ID
    groups = {
        "2362": "Vehicle",
        "2365": "Vehicle",
        "2367": "Vehicle",
        "2370": "Vehicle",
        "2372": "Vehicle",
        "2361": "Pioglitazone",
        "2363": "Pioglitazone",
        "2364": "Pioglitazone",
        "2366": "Pioglitazone",
        "2368": "Pioglitazone",
        "2371": "Pioglitazone",
    }

    # Read the data
    dataframe = read_data(file_path)

    # Compute the averages
    results_df = average_every_10_measurements(dataframe, subject_ids_list, groups)

    # Define the output path
    output_path = os.path.join(os.path.dirname(file_path), "averaged_results.csv")

    # Save the results to the .csv file
    results_df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")
