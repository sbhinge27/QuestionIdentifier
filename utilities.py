import pandas as pd

# Load the datasets
train_df = pd.read_csv('topics.csv')
test_df = pd.read_csv('test.csv')

# Remove the extra column if it exists
train_df = train_df.drop(train_df.columns[2], axis=1)

if '__index_level_0__' in test_df.columns:
    test_df = test_df.drop(columns=['__index_level_0__'])

# Save the cleaned datasets
train_df.to_csv('topics.csv', index=False)
test_df.to_csv('test.csv', index=False)