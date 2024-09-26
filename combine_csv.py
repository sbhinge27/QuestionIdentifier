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

def combine_two(file1, file2):
    import pandas as pd

    data1 = pd.read_csv(file1)

    data2 = pd.read_csv(file2)

    # Combine the two dataframes
    combined_data = pd.concat([data1, data2], ignore_index=True)

    # Save the combined data to a new CSV file
    combined_data.to_csv('question_database.csv', index=False)

    print("CSV files combined successfully!")

# Example usage
# combine_csv_files('sorted_questions.csv', 'question_database.csv')

combine_two('sorted_questions.csv', 'question_database.csv')