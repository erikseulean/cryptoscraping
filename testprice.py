from crypto.libs.price import Price
from datetime import datetime as Date

price = Price()

start_date = Date(2017, 10, 11)
end_date = Date(2017, 12, 11, 17, 30, 00)

print (price.historical("BTC",
        "USD",
        start_date,
        end_date,
        bar_type = "d",
        bar_size = 1,
        num_points = 20,
        exchange = "Bitstamp"))

print (price.historical("BTC",
        "USD",
        start_date,
        end_date,
        bar_type = "d",
        bar_size = 2,
        num_points = 20,
        exchange = "Bitstamp"))

print (
        price.historical(   "ADA",
                            "BTC",
                            Date(2018, 1, 5, 17, 30, 00),
                            bar_type = "m",
                            bar_size = 1,
                            num_points = 30,
                            exchange = "Binance"))

print (
        price.current(      "BTC",
                            "USD",
                            "Bitstamp"))

print (
        price.historical(   "ADA",
                            "BTC",
                            Date(2018, 1, 5, 17, 30, 00),
                            exchange = "Binance"))

print (
        price.historical(   "ADA",
                            "BTC",
                            Date(2018, 1, 1, 17, 30, 00),
                            Date(2018, 1, 5, 17, 30, 00),
                            bar_type = "d",
                            exchange = "Binance"))
