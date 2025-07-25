import pandas as pd

def load_data(path="./data/amazon_delivery.csv"):
    df = pd.read_csv(path)
    print("Dataset loaded with shape:", df.shape)
    print("Columns:", df.columns.tolist())
    return df

def clean_data(df):
    # Remover espaços nos nomes de colunas
    df.columns = df.columns.str.strip()

    # Remover linhas com dados ausentes
    df = df.dropna()
    print("Data cleaned. Remaining rows:", df.shape)

    return df

def basic_stats(df):
    print("\n--- Delivery Time ---")
    print(df['Delivery_Time'].describe())

    print("\n--- By Area ---")
    print(df.groupby('Area')['Delivery_Time'].mean().sort_values())

    print("\n--- By Traffic ---")
    print(df.groupby('Traffic')['Delivery_Time'].mean().sort_values())


if __name__ == "__main__":
    df = load_data()
    df = clean_data(df)
    print(df.head())
