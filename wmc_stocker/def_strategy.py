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


class LongArrangement(Strategy):
    def __init__(self, cash, commission):
        self.__InitMoney = cash
        self.__TotalMoney = cash
        self.__Commission = commission
        self.__ROI = 0
        self.__LocalROI = 0
        self.__Bars = []
        self.__Hold = None
        self.__Profit = 0
        self.__TradingHistory = pd.DataFrame()
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
    def buy(self, data):
        self.__Profit -= data.Close
        currTrade = pd.Series({'Date':data.name, 'Status':"Buy", 'Close':round(data.Close, 2), 'Profit':np.NAN, 'TotalMoney':0, 'ROI(%)':np.NAN})
        self.__TradingHistory = pd.concat([self.__TradingHistory, currTrade], axis = 1)
        # self.__TradingHistoryBuyIdx.append(idx)
        # self.Buy(data)
        self.__Hold = 1

    def sell(self, data):
        # def sell #
        self.__Profit += data.Close

        ### local ROI
        last_close = self.__TradingHistory.iloc[:,-1:].T['Close'].values[0]
        self.__LocalROI = (data.Close - last_close)/last_close
        
        ### TotalMoney
        self.__TotalMoney = self.__TotalMoney*(1 + self.__LocalROI)
        self.__ROI = (self.__TotalMoney - self.__InitMoney)/self.__InitMoney

        currTrade = pd.Series({'Date':data.name, 'Status':"Sell", 'Close':round(data.Close, 2), 'Profit':round(self.__Profit, 2), 'TotalMoney':round(self.__TotalMoney, 2), 'ROI(%)':round(100*self.__ROI, 2)})
        self.__TradingHistory = pd.concat([self.__TradingHistory, currTrade], axis = 1)
        # self.__TradingHistorySellIdx.append(idx)
        # self.Sell(data)
        self.__Hold = None
        
    def next(self, data):
        status = 0
        # long
        if data.Close > data.Open:
            status = +1
        # short
        if data.Close < data.Open:
            status = -1

        # trigger to buy
        if status == +1 and sum(self.__Bars) == -3:
            if self.__Hold is None:
                self.buy(data)

        # trigger to sell
        if status == -1 and sum(self.__Bars) == +3:
            if self.__Hold:
                self.sell(data)

        self.__Bars.append(status)
        if len(self.__Bars) > 3:
            self.__Bars.pop(0)

    def stats(self) -> pd.DataFrame:
        return self.__TradingHistory.T