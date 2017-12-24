## How does it work
1. You come up with a Strategy  
  - The strategy receives a date
  - And outputs a list of tickers you should buy then
2. Then you backtest it over a period of time
  - The backtester calls the strategy for new tickers on every backtestin date
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
            - Initial money to invest, type double
            - Data, type dataframe for all dates and tickers and columns
            - TradingTickers, type list of strings
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
