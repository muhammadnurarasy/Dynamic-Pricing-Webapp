import pandas as pd

# Load the dataset
df = pd.read_csv('Processed_OLX_Used_Car_Dataset_Modified.csv')

# Select 5 random samples from the dataset
sample_inputs = df.sample(5)

# Convert the samples to JSON
sample_inputs_json = sample_inputs.to_json(orient='records')

print(sample_inputs_json)

