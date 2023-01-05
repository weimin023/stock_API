from wmc_stocker.def_strategy import *
from wmc_stocker.top_backtest import *
from wmc_stocker.util import *

stock = YFetcher("006208.TW", "2021-01-01", "2022-01-31")
# stock.Plot()

# backtest


bt = Backtest(stock, LongArrangement,
              cash=50000, commission=.002)


print (bt.run())
bt.plot()
'''
bt.plot()
'''