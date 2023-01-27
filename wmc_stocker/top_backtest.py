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

        self.__stock = stock
        self.__stats = pd.DataFrame
        self.__data: pd.DataFrame = self.__stock.Fetch()
        self.__strategy = strategy(cash, commission)

        self.__ma5  = SMA(self.__data.Close, 5).rename('ma5')
        self.__ma10 = SMA(self.__data.Close, 10).rename('ma10')
        self.__data = pd.concat([self.__data, self.__ma5, self.__ma10], axis = 1)
    
    def run(self) -> pd.DataFrame:
        data = self.__data.copy(deep = False)
        strategy = self.__strategy

        for idx, row in data.iterrows():
            strategy.next(row)

        if (strategy.GetName()=="TangledMA"):
            strategy.next2(self.__data)
        
        self.__stats = strategy.stats()
        return self.__stats

    def plot(self):
        # add indicators
        return self.__stock.Plot(self.__stats)
        