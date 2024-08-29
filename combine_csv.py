import os
import pandas as pd

def combine_csv_files(input_directory, output_file):
    # List to store DataFrames
    data_frames = []
    
    # Read all CSV files in the specified directory
    for file_name in os.listdir(input_directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_directory, file_name)
            df = pd.read_csv(file_path)
            data_frames.append(df)
    
    # Combine all DataFrames into a single DataFrame
    combined_df = pd.concat(data_frames, ignore_index=True)
    
    # Write the combined DataFrame to the output file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV file saved as {output_file}")

# Example usage
combine_csv_files('qa', 'question_database.csv')
