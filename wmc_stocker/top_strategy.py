from abc import abstractmethod
import pandas as pd
import numpy as np

class Strategy():
    def __init__(self, cash, commission):
        self._InitMoney = cash
        self._TotalMoney = cash
        self._Commission = commission
        self._ROI = 0
        self._LocalROI = 0
        self._Bars = []
        self._Hold = None
        self._Profit = 0
        self._TradingHistory = pd.DataFrame()
    
    def stats(self) -> pd.DataFrame:
        return self._TradingHistory.T

    @abstractmethod
    def next(self, data):
        return NotImplemented

    def Buy(self, data):
        self._Profit -= data.Close
        currTrade = pd.Series({'Date':data.name, 'Status':"Buy", 'Close':round(data.Close, 2), 'Profit':np.NAN, 'TotalMoney':0, 'ROI(%)':np.NAN})
        self._TradingHistory = pd.concat([self._TradingHistory, currTrade], axis = 1)

        self._Hold = 1

    def Sell(self, data):
        # def sell #
        self._Profit += data.Close

        ### local ROI
        last_close = self._TradingHistory.iloc[:,-1:].T['Close'].values[0]
        self._LocalROI = (data.Close - last_close)/last_close
        
        ### TotalMoney
        self._TotalMoney = self._TotalMoney*(1 + self._LocalROI)
        self._ROI = (self._TotalMoney - self._InitMoney)/self._InitMoney

        currTrade = pd.Series({'Date':data.name, 'Status':"Sell", 'Close':round(data.Close, 2), 'Profit':round(self._Profit, 2), 'TotalMoney':round(self._TotalMoney, 2), 'ROI(%)':round(100*self._ROI, 2)})
        self._TradingHistory = pd.concat([self._TradingHistory, currTrade], axis = 1)

        self._Hold = None



        

def compute_stats():
    #TODO
    return NotImplemented