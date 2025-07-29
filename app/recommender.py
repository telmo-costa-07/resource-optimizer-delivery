
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np

# Features to use for recommendation (excluding 'Vehicle')
RECOMMENDER_FEATURES = [
    'Agent_Age', 'Agent_Rating', 'Store_Latitude', 'Store_Longitude',
    'Drop_Latitude', 'Drop_Longitude', 'Weather', 'Traffic', 'Area'
]

def train_vehicle_recommender(df):
    """
    Trains a model for each vehicle type to predict delivery time, using the given features.
    Returns a dict of vehicle type to trained pipeline.
    """
    vehicle_types = df['Vehicle'].unique()
    models = {}
    for vehicle in vehicle_types:
        # Create a binary target: 1 if this vehicle, 0 otherwise
        df_vehicle = df.copy()
        df_vehicle['IsVehicle'] = (df_vehicle['Vehicle'] == vehicle).astype(int)
        # Only use rows with this vehicle for regression
        X = df_vehicle[df_vehicle['IsVehicle'] == 1][RECOMMENDER_FEATURES]
        y = df_vehicle[df_vehicle['IsVehicle'] == 1]['Delivery_Time']
        # Preprocessing: numeric/categorical
        numeric_features = ['Agent_Age', 'Agent_Rating', 'Store_Latitude', 'Store_Longitude',
                            'Drop_Latitude', 'Drop_Longitude']
        categorical_features = ['Weather', 'Traffic', 'Area']
        preprocessor = ColumnTransformer([
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor())
        ])
        pipeline.fit(X, y)
        models[vehicle] = pipeline
    return models

def recommend_vehicle(input_features, models):
    """
    Given input features (dict or DataFrame), returns the vehicle type with the lowest predicted delivery time.
    """
    if isinstance(input_features, dict):
        input_df = pd.DataFrame([input_features])[RECOMMENDER_FEATURES]
    else:
        input_df = input_features[RECOMMENDER_FEATURES]
    best_vehicle = None
    best_time = np.inf
    predictions = {}
    for vehicle, model in models.items():
        pred_time = model.predict(input_df)[0]
        predictions[vehicle] = pred_time
        if pred_time < best_time:
            best_time = pred_time
            best_vehicle = vehicle
    return best_vehicle, best_time, predictions
