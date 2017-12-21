from mush import Runner
from page_loader import load
from coin_scrapping import scrap_coins
from exchange_scrapping import scrap_exchanges
from parallel_scrap import go_get_them
from cleanup import top100_cleanup
from google_trends import get_all_trends

if __name__ == "__main__":
    
    runner = Runner()
    runner.add(load)
    runner.add(scrap_coins)
    runner.add(go_get_them)
    runner.add(scrap_exchanges)
    runner.add(top100_cleanup)
    runner.add(get_all_trends)

    runner()