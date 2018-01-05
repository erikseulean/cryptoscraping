from portfolio import Portfolio
import analytics
import utils

class Backtester:
    def __init__(self, data, model, startDate, endDate, rebalanceEvery, initialCash):
        self.data = data
        self.model = model
        self.startDate = startDate
        self.endDate = endDate
        self.rebalanceEvery = rebalanceEvery
        self.initialCash = initialCash

    def run(self, verbose=False):

        portfolio = Portfolio(self.data, self.startDate, [], self.initialCash)
        rebalanceFreq, rebalancePer = self.rebalanceEvery

        daterange = utils.dateRange(self.startDate, self.endDate, rebalanceFreq, rebalancePer)
        for date in daterange:
            # 1. Data precalculation
            dataDate = analytics.getDate(self.data, date)
            # 2. print stats at date
            portfolio.runReport(date, verbose = verbose)
            # 3. sell all coins bought last period
            portfolio.liquidate(dataDate, date)

            # 4. buy new coins
            holdings = []
            coins = self.model.generateCoins(date)
            if coins is not None:

                amountPerCoin = portfolio.cash / len(coins)
                for coin in coins:
                    try:
                        priceCoin = analytics.getClose(dataDate, coin, date)
                        numCoins = amountPerCoin / priceCoin
                        #print ("Buying coin {} at price {} amount {}".format(coin, priceCoin, numCoins))
                        holdings.append({"Coin":coin, "Position": numCoins, "Bought at": priceCoin})
                    except:
                        print ("Coin {} no longer exists as of {}".format(
                                coin, date))

            portfolio = Portfolio(self.data, date, holdings, 0)

        portfolio.liquidate(dataDate, date)
        finalCash = portfolio.cash

        totalProfit = round(finalCash - self.initialCash, 3)
        totalReturn = round((finalCash/self.initialCash - 1) * 100, 3)
        print ("Invested {} Cashed out {} Profit ${} Return {}%".format(
                self.initialCash, finalCash, totalProfit, totalReturn))
