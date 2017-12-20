from multiprocessing import Pool, cpu_count
from joblib import Parallel, delayed
import pandas as pd
from historical_data import get_historical_data

def go():

    num_cores = cpu_count()

    df = pd.DataFrame.from_csv('coins.csv')

    get_historical_data(df['Coins'][0], mode = 'w', include_header=True)
    
    with Pool(processes=num_cores) as pool:
        pool.map(get_historical_data, df['Coins'][1:100])


if __name__ == "__main__":
    go()
