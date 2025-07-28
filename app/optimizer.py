import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

FEATURES = [
    'Agent_Age', 'Agent_Rating', 'Store_Latitude', 'Store_Longitude',
    'Drop_Latitude', 'Drop_Longitude', 'Weather', 'Traffic', 'Vehicle', 'Area'
]
TARGET = 'Delivery_Time'
NUMERIC_FEATURES = [
    'Agent_Age', 'Agent_Rating', 'Store_Latitude', 'Store_Longitude',
    'Drop_Latitude', 'Drop_Longitude'
]
CATEGORICAL_FEATURES = ['Weather', 'Traffic', 'Vehicle', 'Area']

def train_delivery_time_model(df):
    """
    Treina um modelo de ML para prever o Delivery_Time.
    Retorna o pipeline treinado e o MSE no conjunto de teste.
    """
    X = df[FEATURES]
    y = df[TARGET]

    # Pipeline para transformar dados
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', NUMERIC_FEATURES),
            ('cat', OneHotEncoder(handle_unknown='ignore'), CATEGORICAL_FEATURES)
        ]
    )

    model_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor())
    ])

    # Separar treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar modelo
    model_pipeline.fit(X_train, y_train)

    # Avaliar
    y_pred = model_pipeline.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    return model_pipeline, mse
