from abc import abstractmethod
import pandas as pd
from wmc_stocker.def_strategy import Strategy
from wmc_stocker.util import *

class Backtest:
    def __init__(self,
                 stock: Fetcher,
                 strategy: Strategy,
                 cash: float = 10_000,
                 commission: float = .0):
        self.__stock = stock
        self.__stats = pd.DataFrame
        self.__data: pd.DataFrame = self.__stock.Fetch()
        self.__strategy = strategy(cash, commission)
    
    def run(self) -> pd.DataFrame:
        data = self.__data.copy(deep = False)
        strategy = self.__strategy
        
        for idx, row in data.iterrows():
            strategy.next(row)
        self.__stats = strategy.stats()
        return self.__stats

    def plot(self):
        # add indicators
        return self.__stock.Plot(self.__stats)
        