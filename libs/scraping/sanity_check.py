import pandas as pd

def test_valid_inputs():
    coins = pd.DataFrame.from_csv('coins.csv')
    
    assert(len(coins['Coins']) == 1368) #includes header

    all_data = pd.read_csv(
        'coin_data.csv',
        header=0,
        low_memory=False, 
        encoding='utf-8-sig',
        index_col=None,
        delimiter=','
    )

    unique_from_dataset = set(all_data['Coin'].unique())
    assert len(unique_from_dataset) >= 100
