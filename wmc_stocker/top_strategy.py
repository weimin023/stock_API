from abc import abstractmethod
import pandas as pd

class Strategy():
    # def __init__(self, broker, data, params):

    @abstractmethod
    def next(self, data):
        return NotImplemented

    @abstractmethod
    def Buy(self):
        return NotImplemented
        print ("[Buy]")
        print (data.name)
        print (self.Profit)

    @abstractmethod
    def Sell(self):
        return NotImplemented
        print ("[Sell]")
        print(data)



        

def compute_stats():
    #TODO
    return NotImplemented