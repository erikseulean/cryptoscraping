import analytics
import pandas as pd

class StrategyTopMarketCap:
    def __init__(self, data):
        self.data = data
    def generateCoins(self, date, allowedCoins = None):
        dataDate = analytics.getDate(self.data, date)
        dataDate = analytics.getSorted(dataDate, "Market-Cap", asc=False)
        return dataDate.head(10)["Coin"]

class StrategyTopTenofTopOneHundredMarketCapUnderTwentyCents:
    def __init__(self, data):
        self.data = data
    def generateCoins(self, date, allowedCoins = None):
        dataDate = pd.DataFrame(self.data)
        dataDate = analytics.getDate(dataDate, date)
        dataDate["ClosePx"] = pd.to_numeric(dataDate["Close"])
        dataDate = dataDate[(dataDate["ClosePx"] < 0.2)]
        dataDate = analytics.getSorted(dataDate, "Market-Cap")
        return dataDate.head(10)["Coin"]

class StrategyBottomTenofTopOneHundredMarketCapUnderTwentyCents:
    def __init__(self, data):
        self.data = data
    def generateCoins(self, date, allowedCoins = None):
        dataDate = pd.DataFrame(self.data)
        dataDate = analytics.getDate(dataDate, date)
        dataDate["ClosePx"] = pd.to_numeric(dataDate["Close"])
        dataDate = dataDate[(dataDate["ClosePx"] < 0.2)]
        dataDate = analytics.getSorted(dataDate, "Market-Cap")
        return dataDate.head(100).tail(10)["Coin"]

class StrategyBottomTenofTopOneHundredMarketCapUnderTwoMil:
    def __init__(self, data):
        self.data = data
    def generateCoins(self, date, allowedCoins = None):
        dataDate = analytics.getDate(self.data, date)
        dataDate = dataDate[(dataDate["Market-Cap"] < 200000000)]
        dataDate = analytics.getSorted(dataDate, "Market-Cap", asc=False)
        return dataDate.head(100).tail(10)["Coin"]

class StrategyBottomTenofTopOneHundredMarketCap:
    def __init__(self, data):
        self.data = data
    def generateCoins(self, date, allowedCoins = None):
        dataDate = analytics.getDate(self.data, date)
        dataDate = analytics.getSorted(dataDate, "Market-Cap", asc=False)
        return dataDate.head(100).tail(10)["Coin"]
