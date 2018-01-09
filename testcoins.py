from crypto.libs.coins import Coins
from crypto.libs.marketcap import MarketCap
from crypto.libs.price import Price


from datetime import datetime as Date

coins = Coins()
#marketcap = MarketCap()
price = Price()

ico_date =  coins.coin_data(coin, {"field":"ICO"})
roi = price.change("bitcoin", "usd", ico_date, Date(2018, 1, 5))
