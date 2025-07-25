import pandas as pd

def load_data(path="./data/amazon_delivery.csv"):
    df = pd.read_csv(path)
    print("Dataset loaded with shape:", df.shape)
    print("Columns:", df.columns.tolist())

    df.info()
    return df

def clean_data(df):
    # Remove spaces from column names
    df.columns = df.columns.str.strip()

    df.isnull().sum()

    # Remove rows with missing data
    df = df.dropna()
    print("Data cleaned. Remaining rows:", df.shape)

    return df

if __name__ == "__main__":
    df = load_data()
    df = clean_data(df)
    print(df.head())
