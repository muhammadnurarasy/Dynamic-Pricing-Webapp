from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import joblib
import pandas as pd
import numpy as np 

# Initialize the FastAPI app
app = FastAPI()

# Load the trained model
model = joblib.load('ml_model/trained_model.pkl')

# Define a data model for the input data
class RealEstateInput(BaseModel):
    Property_Type: str
    Property_Size: int
    Bedrooms: int
    Bathrooms: int
    Location: str
    Furnishing: str
    Age_of_Property: Optional[int] = None
    Amenities: str
    Proximity_to_Important_Locations: Optional[float] = None
    Floor_Level: int
    Property_Status: str

@app.post("/predict")
def predict_price(data: RealEstateInput):
    # Convert input data to dataframe
    data_df = pd.DataFrame([dict(data)])
    
    # Handle NaN values
    if data.Age_of_Property is None:
        data_df['Age_of_Property'] = np.nan
    if data.Proximity_to_Important_Locations is None:
        data_df['Proximity_to_Important_Locations'] = np.nan

    # Predict using the model
    try:
        predicted_price = float(model.predict(data_df)[0])  # Convert prediction to native Python float
        return {"predicted_price": predicted_price}
    except:
        raise HTTPException(status_code=400, detail="Error predicting the price. Ensure the input data is correct.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
