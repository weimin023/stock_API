from wmc_stocker.top_strategy import *
from wmc_stocker.math_util import *
from backtesting.lib import *
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class SmaCross(Strategy):
    def __init__(self):
        price = self.data.Close
        self.ma1 = SMA(price, 10)
        self.ma2 = SMA(price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
            print(1)
        elif crossover(self.ma2, self.ma1):
            self.sell()
            print(2)
'''
class TangledMA(Strategy):
    def __init__(self, cash, commission):

'''
class LongArrangement(Strategy):
    #def __init__(self, cash, commission):
        
        # self.__TradingHistoryBuyIdx = []
        # self.__TradingHistorySellIdx = []
    '''
        self.data = data
        self.ma1 = SMA(data.Close, 5)
        self.ma2 = SMA(data.Close, 10)
    '''
    '''
    def plot(self):
        sns.lineplot(self.ma1, marker="o")
        sns.lineplot(self.data.Close, marker="o")
        plt.legend(labels=["ma1","close"])
        plt.grid()
        plt.show()
    '''
    
    def next(self, data):
        status = 0
        # long
        if data.Close > data.Open:
            status = +1
        # short
        if data.Close < data.Open:
            status = -1

        # trigger to buy
        if status == +1 and sum(self._Bars) == -3:
            if self._Hold is None:
                self.Buy(data)

        # trigger to sell
        if status == -1 and sum(self._Bars) == +3:
            if self._Hold:
                self.Sell(data)

        self._Bars.append(status)
        if len(self._Bars) > 3:
            self._Bars.pop(0)

    