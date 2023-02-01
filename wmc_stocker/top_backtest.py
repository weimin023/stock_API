from abc import abstractmethod
import pandas as pd
from wmc_stocker.def_strategy import Strategy
from wmc_stocker.util import *
import numpy as np

class Backtest:
    def __init__(self,
                 stock: Fetcher,
                 strategy: Strategy,
                 cash: float = 10_000,
                 commission: float = .0):

        self._stock = stock
        self._data: pd.DataFrame = self._stock.Fetch()
        self._strategy = strategy(self._data, cash, commission)

    def run(self) -> pd.DataFrame:
        strategy = self._strategy
        strategy.next()
        
        self._stats = strategy.GetTradingHistory()
        return self._stats

    def plot(self):
        plot = Plotter(self._data, self._stock.GetName())

        # plot return figure
        fig = plot.GetFig()

        # add indicators to figure by strategies
        StrategyName = self._strategy.GetName()
        if StrategyName == "TangledMA":
            TECHINDI = self._strategy.GetTechIndicator()
            BLUE_X = []
            BLUE_Y = []
            RED_X  = []
            RED_Y  = []
            for k, v in TECHINDI.items():
                RED_X.append(k)
                RED_Y.append(self._data.loc[k].High)
                for i in range(0, 3):
                    BLUE_X.append(v[0][i][0])
                    BLUE_Y.append(self._data.loc[v[0][i][0]].High)
            
            fig.scatter(BLUE_X, BLUE_Y, size = 20, marker = "inverted_triangle", fill_color="dodgerblue")
            fig.scatter(RED_X, RED_Y,   size = 20, marker = "square_pin", fill_color="magenta")
        '''if (=="TangledMA"):
            triggeredTradeList = self._data.loc[indicator['Date']]
            cnt = 0
            for idx, row in triggeredTradeList.iterrows():
                if cnt%2 == 0:
                    self.BuyIndicator(candlestick, idx, row['High'])
                else:
                    self.SellIndicator(candlestick, idx, row['Low'])
                cnt += 1
            
            for idx, row in triggeredTradeList.iterrows():
                self.BuyIndicator(fig, idx, row['High'])'''

        return plot.GetPlot()
        