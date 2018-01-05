import pandas as pd
from datetime import date

def cleanup():
        all_data = pd.read_csv(
                'crypto/data/coin_data.csv',
                header=0,
                low_memory=False, 
                encoding='utf-8-sig',
                index_col=0,
                delimiter=','
        )

        all_data['Date'] = all_data['Date'].str.replace('.', '')
        all_data['Volume'] = all_data['Volume'].str.replace('.', '')
        all_data['Market-Cap'] = all_data['Market-Cap'].str.replace('.', '')
        all_data['Date'] = pd.to_datetime(all_data['Date'], errors='coerce')
        all_data.to_csv('crypto/data/coin_data_cleaned.csv')


