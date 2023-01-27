from wmc_stocker.top_strategy import *
from wmc_stocker.math_util import *
from backtesting.lib import *
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime

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

class TangledMA(Strategy):
    def __init__(self, *args, **kwargs):
        super(TangledMA, self).__init__(*args, **kwargs)
        self.CrossPts = []
        self.last     = 0

    def GetName(self)->str:
        return "TangledMA"

    def next(self, data: pd.DataFrame):
        if data.ma5 > data.ma10:
            status = +1
        else:
            status = -1

        # if cross occur, append the crosspoint
        if (self.last + status)==0:
            self.CrossPts.append(data.name)
        else:
            pass

        self.last = status
    
    def next2(self, data: pd.DataFrame):
        cross = pd.DataFrame(self.CrossPts)
        
        # if cross points number < 3
        pNum = cross.shape[0]
        if pNum < 3: return
            
        for p in range(2, pNum):
            third_ = cross.iloc[p] + datetime.timedelta(days=1)
            first_ = cross.iloc[p-2]
            dDiff = ((third_-first_)/np.timedelta64(1, 'D')).astype(int)[0]
            if (dDiff) <= 30:
                end_ = third_ + datetime.timedelta(days=30)
                target = data.loc[first_].Close
                range_data = data.loc[third_[0]:end_[0]].Close

                toTrade = range_data[range_data>target[0]].index
                if (toTrade.empty): continue
                self.Buy(data.loc[toTrade[0]])
    
        



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
    def GetName(self)->str:
        return "LongArrangement"
    
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

    