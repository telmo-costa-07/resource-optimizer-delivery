# Otimizador de modelo ML para previsão de Delivery_Time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def train_delivery_time_model(df):
    features = ['Agent_Age', 'Agent_Rating', 'Store_Latitude', 'Store_Longitude', 
                'Drop_Latitude', 'Drop_Longitude', 'Weather', 'Traffic', 'Vehicle', 'Area']
    target = 'Delivery_Time'

    # Codificar variáveis categóricas
    df_encoded = pd.get_dummies(df[features])
    X = df_encoded
    y = df[target]

    # Separar treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar modelo
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Avaliar
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    return model, mse
