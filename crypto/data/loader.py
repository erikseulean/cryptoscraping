import pandas as pd

def cleaned_dataset():
    data = pd.read_csv(
        'crypto/data/coin_data_cleaned.csv',
        header=0,
        low_memory=False,
        encoding='utf-8-sig',
        delimiter=','
    )
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Market-Cap'] = pd.to_numeric(data['Market-Cap'], errors='coerce')
    data['Volume'] = pd.to_numeric(data['Volume'], errors='coerce')
    data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
    data = data.drop_duplicates()
    return data