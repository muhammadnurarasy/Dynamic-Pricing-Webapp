import pandas as pd
import numpy as np

data = pd.read_csv('real_estate_dynamic_pricing/ml_model/Data.csv')

# Select core features
simplified_data = data[['Property_Size', 'Bedrooms', 'Bathrooms', 'Location', 'Furnishing', 'Price']].copy()

# Simulate historical prices
simplified_data['Historical_Price'] = simplified_data['Price'] * (1 + np.random.uniform(-0.1, 0.1, simplified_data.shape[0]))

# Generate random dates for Date_of_Listing
simplified_data['Date_of_Listing'] = pd.date_range(start='2020-01-01', periods=simplified_data.shape[0], freq='7D')

# Shuffle the rows
simplified_data = simplified_data.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to CSV
simplified_data.to_csv('simplified_real_estate_data.csv', index=False)
