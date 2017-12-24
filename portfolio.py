import analytics
import utils
import datetime
import pandas as pd

class Portfolio:
    def __init__(self, data, creationDate, holdings, cash):
        self.holdings = holdings
        self.creationDate = creationDate
        self.data = data
        self.cash = cash
        self.report = None

    def liquidate(self, dataDate, date):
        pv = 0.0
        for holding in self.holdings:
            coin = holding["Coin"]
            position = holding["Position"]
            priceCoin = 0.0
            try: # might have ceased to exist
                priceCoin = analytics.getClose(dataDate, coin, date)
            except:
                print ("Coin {} no longer exists as of {}".format(
                        coin, date))

            pv += priceCoin * position
        self.holdings = []
        self.cash += pv

    def runReport(self, reportDate, verbose=False):

        if len(self.holdings) == 0:
            return

        report, pvAtCreationDate, pvAtReportDate, pvChange, pvChangePct = \
            self.createReport(reportDate)

        if verbose:
            print ("Report for period {} to {}".format(
                    self.creationDate, reportDate))
            print ("PV at creation {} at report {} chg ${} pct {}%".format(
                    pvAtCreationDate, pvAtReportDate, pvChange, pvChangePct))

            return report
        else:
            print ("Report {} to {}, PV from {} to {}, chg ${} pct {}%".format(
                    self.creationDate, reportDate,
                    pvAtCreationDate, pvAtReportDate,
                    pvChange, pvChangePct))

    def createReport(self, reportDate):

        pvAtCreationDate = 0.0
        pvAtReportDate = 0.0
        pvChangePct = 0.0

        portfolioData = []
        for holding in self.holdings:
            coin = holding["Coin"]
            coinPosition = holding["Position"]

            coinPriceAtCreationDate = holding["Bought at"]
            coinPriceAtReportDate = 0.0
            try:
                # might have ceased to trade
                coinPriceAtReportDate = analytics.getClose(self.data, coin, reportDate)
            except:
                print ("Coin {} no longer exists as of {}".format(
                        coin, reportDate))

            coinPriceChange = coinPriceAtReportDate - coinPriceAtCreationDate
            coinProfit = coinPosition * (coinPriceChange)
            coinPvAtCreationDate = coinPosition * coinPriceAtCreationDate
            coinPvAtReportDate = coinPosition * coinPriceAtReportDate
            coinProfitPct = ((coinPvAtReportDate/coinPvAtCreationDate) - 1) * 100

            pvAtCreationDate += coinPvAtCreationDate
            pvAtReportDate += coinPvAtReportDate

            portfolioData.append({"Coin": coin,
                        "Position": coinPosition,
                        "Purchase Price": coinPriceAtCreationDate,
                        "Current Price": coinPriceAtReportDate,
                        "Price change": coinPriceChange,
                        "PV at purchase": coinPvAtCreationDate,
                        "PV current": coinPvAtReportDate,
                        "Return $": coinProfit,
                        "Return %": coinProfitPct})

        # Create Report Dataframe
        cols = ["Coin", "Position", "Purchase Price", "Current Price", "Price change",
                "PV at purchase", "PV current", "Return $", "Return %"]
        df = pd.DataFrame(portfolioData, columns = cols)

        # Calculate overall analytics
        pvChange = pvAtReportDate - pvAtCreationDate
        if pvAtCreationDate != 0:
            pvChangePct = (pvAtReportDate/pvAtCreationDate - 1) * 100

        return (df,
                round(pvAtCreationDate,3),
                round(pvAtReportDate,3),
                round(pvChange,3),
                round(pvChangePct,3))
