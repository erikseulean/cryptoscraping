Classes:
    - Backtester
        Inputs:
            - Initial money to invest, type double
            - Data, type dataframe for all dates and tickers and columns
            - TradingTickers, type list of strings
            - StartDate, type: datetime.date
            - EndDate, type: datetime.date
            - RebalancingFrequency, type: int, expresssed as number of days, default = 14
            - ProfitCalculationFrequency, type: int, expressed as number of days, default = 14
            - StrategySelector
        Outputs:
            - Total profit in dollars
            - Total profit in %
            - Total profit per ticker
            - Profit broken down by period and ticker

    - StrategySelector (Parent Class)
        Input:
            - Date
            - TradingTickers, type list of strings
        Output:
            - Buy Tickers, type list of strings
            - Sell Tickers, type list of strings

        Children classes (implementations):
        - Deep Neural Network
        - Random Forest
        - Top 10 Market Cap Selector
