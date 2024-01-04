import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

# Load the dataset
df = pd.read_csv('Cleaned_Combined_OLX_Used_Car_Dataset.csv')

# One-hot encoding for 'brand' and 'type'
encoder = OneHotEncoder(sparse_output=False)
encoded_cols = encoder.fit_transform(df[['brand', 'type']])
encoded_cols_df = pd.DataFrame(encoded_cols, columns=encoder.get_feature_names_out(['brand', 'type']))

# Define mileage rankings
mileage_rankings = {
    '5.000': 34,
    '5.000-10.000': 33,
    '10.000-15.000': 32,
    '15.000-20.000': 31,
    '20.000-25.000': 30,
    '25.000-30.000': 29,
    '30.000-35.000': 28,
    '35.000-40.000': 27,
    '40.000-45.000': 26,
    '45.000-50.000': 25,
    '50.000-55.000': 24,
    '55.000-60.000': 23,
    '60.000-65.000': 22,
    '65.000-70.000': 21,
    '70.000-75.000': 20,
    '75.000-80.000': 19,
    '80.000-85.000': 18,
    '85.000-90.000': 17,
    '90.000-95.000': 16,
    '95.000-100.000': 15,
    '100.000-105.000': 14,
    '105.000-110.000': 13,
    '110.000-115.000': 12,
    '115.000-120.000': 11,
    '120.000-125.000': 10,
    '125.000-130.000': 9,
    '130.000-135.000': 8,
    '135.000-140.000': 7,
    '140.000-145.000': 6,
    '145.000-150.000': 5,
    '150.000-155.000': 4,
    '155.000-160.000': 3,
    '160.000-165.000': 2,
    '165.000-170.000': 1
}

# Convert mileage to ranks
df['mileage_rank'] = df['mileage'].map(mileage_rankings)

# Scale 'year' and 'price'
scaler = MinMaxScaler()
df[['year', 'price']] = scaler.fit_transform(df[['year', 'price']])

# Combine the processed data
processed_df = pd.concat([df, encoded_cols_df], axis=1)

# Drop original columns
processed_df.drop(columns=['brand', 'type', 'mileage'], inplace=True)

# Save the processed data
processed_csv_path = 'Processed_OLX_Used_Car_Dataset.csv'
processed_df.to_csv(processed_csv_path, index=False)

# Print the first few rows to verify
print(processed_df.head())


# Input the preprocessed dataset into google ai studio vertex ML automation