## TODO:
The end goal is to have the following structure working well:
  - data (contains either a database or a filesystem that gets automatically updated)
  - libs (contains all the price, market cap, model, backtesting, portfolio) core functionality
  - analytics (building tools out of libs)
  - notebooks (like a dashboard where we can see different things)

Data seems the most urgent one since everything is built on top of that. We need to automate it.

### Data that we need:
- historical and current prices per coins - daily, hourly, minute
- historical and current market cap for all coins - not only 100 and not only a few days. all history.

### Libs that we need:
```
import libs.coins as coins
import libs.pairs as pairs
import libs.price as price
import libs.marketcap as marketcap

import libs.book as book
import libs.portfolio as portfolio
import libs.models as models
import libs.backtesting as backtesting
```

### Analytics that we need:
```
import analytics.dashboard as dashboard
import analytics.macro as macro
import analytics.coininfo as coininfo
import analytics.coinperformance as coinperformance
import analytics.bookperformance as bookperformance

import analytics.signals
import analytics.alerts
```

### Notebooks that we need:
```
Portfolio performance analysis
Coin performance analysis
Coin Pair performance analysis
Macro coin market overview
Signals & Alerts
Strategy testing and analysis
```

## Getting data
We're scrapping [coinmarketcap](coinmarketcap.com) to get the list of coins and we get all their historical data.
In order to generate all the data run: 
```py
from crypto.libs.scraping.refresh import run
run()
```
This will create a couple of files:
- `all_cryptos.html` - the main page that we scrap. Because this has over 1600 coins, we save it locally so we don't fetch it everytime we run the script
- `coins.csv` - list of all coins available today on the site
- `coin_data.csv` - all historical data for the coins fetched in `coins.csv`
- `coin_data_cleaned.csv` - cleanup of the `coind_data.csv` file, in terms of empty values, dates formating or types
- `coin_trends.csv` - google trends on the given list of coins. We check the correlation between the trending values for that term and the coin price

## How does it work
1. You come up with a Strategy  
  - The strategy receives a date
  - And outputs a list of tickers you should buy then

2. Then you backtest it over a period of time
  - The backtester calls the strategy for new tickers on every backtesting date
  - And buys those coins, and sells what it previously bought a period before

## How to run

```py
import datetime
import pandas as pd
import numpy as np
import utils
import analytics
import portfolio
import backtester
import models

# please make sure you only run this once!
# import refresh
# refresh.run()
data = analytics.cleaned_dataset()

model = models.StrategyBottomTenofTopOneHundredMarketCapUnderTwentyCents(data)
startDate = datetime.date(2017, 1, 1)
endDate = datetime.date(2017, 12, 22)
initialCash = 100

tester = backtester.Backtester(data, model, startDate, endDate, (1, "m"), initialCash)
tester.run(verbose=False)

```

## Classes:
    - Backtester
      -  Inputs:
            - Initial money to invest, type: double
            - Data, type: dataframe for all dates and tickers and columns
            - TradingTickers, type: list of strings
            - StartDate, type: datetime.date
            - EndDate, type: datetime.date
            - RebalancingFrequency, type: int, expresssed as number of days, default = 14
            - ProfitCalculationFrequency, type: int, expressed as number of days, default = 14
            - StrategySelector

      -  Outputs:
            - Total profit in dollars
            - Total profit in %
            - Total profit per ticker
            - Profit broken down by period and ticker

    - StrategySelector (Parent Class)
      -  Input:
            - Date
            - TradingTickers, type list of strings

      -  Output:
            - Buy Tickers, type list of strings
            - Sell Tickers, type list of strings

      -  Children classes (implementations):
        - Deep Neural Network
        - Random Forest
        - Top 10 Market Cap Selector
        - Bottom 10 prices under 20 cents within top 100 market cap

## How to come up with a strategy

The Process:

I. Analyse the entire market to come up with a list of tickers
```
  1. Search for seasonality (monthly and weekly and annually)
    - look at Christmas spike and January deflation
  2. Look at the correlation matrix
    - see which go together and when
    - look for the lag behind different coins, i.e. is eth correlated with btc + 1day?

  3. Group by sectors
  4. Group by market cap
  5. Calculate volatilty
  6. Plot the volatility profile of the market
  7. Plot the volatility profile different coins
  8. How many coins % of total have EVER doubled their price = pump
  9. Look at new comers in top 100!
  10. See price increase of poloniex/bittrex/binance exchange coins from beginning of listing
  11. Pace of new account openings
```
II. Analyse a portfolio of coins coming up from 1.
```
  1. Backtesting monthly, weekly, daily
  2. Look for correlation matrix and volatilty of the portfolio
  3. Backtest vs usd and vs btc
```

III. Individual coin analysis
```
  1. look at full history of price (search for pumps and dumps)
    - vs USD and vs BTC
  2. look at recent history of price (search for pumps and dumps)
    - vs USD and vs BTC
  3. look at market cap (should be highly correlated with price)
    - check for growth as % of entire market
    - check if you make money vs the market not vs the dollar
    - otherwise you have opportunity cost
    - need to have benchmark.
  4. look how it grows depending on exchange adoption
  5. profile diff coins based on google trends, reddit, twitter
  6. search for pumps as % of initial price so the pump is yet to come
  7. find the average life of an altcoin (drop below issue price = death)
  8. When it was adopted by exchange analysis
```

IV. Investing strategy
```
  1. Stop loss order
  2. Cash out
```

V. Strategy ideas:
```
  1. shower thoughts: buy every <1000sat coin on bittrex (there are around 8) and put a sell order for 2x. come back after 8 days. you will have 2x in your wallet most probably.😂😂
  2. buy btc and aftD it grow 10% buy altcoins and after
  they rise 10% buy btc. pairs trading basically
```

TODO:
    - Intraday data - see here https://github.com/agalea91/cryptocompare-api/blob/master/CryptoCompare.API.2017.08.ipynb
    - Attribution of portfolio losses and gains based on the coin - stacked bars
    - strategy for swing trading (buy low sell high vs btc and eth)
