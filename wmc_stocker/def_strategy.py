from wmc_stocker.top_strategy import *
from wmc_stocker.math_util import *
from backtesting.lib import *
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime
from collections import defaultdict

'''class SmaCross(Strategy):
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
            print(2)'''

class TangledMA(Strategy):
    def __init__(self, *args, **kwargs):
        super(TangledMA, self).__init__(*args, **kwargs)
        self._CrossPts = []
        self._last     = 0
        ### save each pair of cross pts into dict
        ### ex: {"1st buy point": 1st cross, 2nd cross, 3rd cross, 
        ###      "2nd buy point": 1st cross, 2nd cross, 3rd cross,...}
        self._DictCrossBuy = defaultdict(list)

    def GetName(self)->str:
        return "TangledMA"

    def GetTechIndicator(self):
        return self._DictCrossBuy

    def next(self):
        data: pd.DataFrame = self._data

        ### STEP1. Find out all of the cross pts
        for idx, row in data.iterrows():
            if row.ma5 > row.ma10:
                status = +1
            else:
                status = -1

            # if cross occur, append the crosspoint
            if (self._last + status)==0:
                self._CrossPts.append(row.name)
            else:
                pass

            self._last = status
            
        #### STEP2. Find each pair of cross pts
        cross = pd.DataFrame(self._CrossPts)
        

        # if cross points number < 3
        pNum = cross.shape[0]
        if pNum < 3: return
            
        for p in range(2, pNum):
            # cross pts
            first_, second_, third_ = cross.iloc[p-2], cross.iloc[p-1], cross.iloc[p]

            # the VALID duration of each pair of cross pts should within 30 days
            dDiff = ((third_-first_)/np.timedelta64(1, 'D')).astype(int)[0]
            if (dDiff) <= 30:
                end_ = third_ + datetime.timedelta(days=30)
                target = data.loc[first_].Close

                # the search range should except "the third day of each pair"
                range_data = data.loc[third_[0] + datetime.timedelta(days=1):end_[0]].Close

                # the "BUY POINT" is the point:
                # 1. larger than 1st point of each pair
                # 2. within 30 days after the 3rd cross point of each pair
                toTrade = range_data[range_data > target[0]].index

                if (toTrade.empty): continue
                self.Buy(data.loc[toTrade[0]])

                self._DictCrossBuy[toTrade[0]].append([first_, second_, third_])
        
    


    