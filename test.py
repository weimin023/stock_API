from wmc_stocker.def_strategy import *
from wmc_stocker.top_backtest import *
from wmc_stocker.util import *

import unittest
import time
import multiprocessing as mp
import sqlite3

class APITestCase(unittest.TestCase):
    def test_GenTangledMAImg(self):
        stock = YFetcher('2330.TW', "2022-10-01", "2022-12-01")
        bt = Backtest(stock, TangledMA, cash=50000, commission=.002)
        bt.run()
        bt.plot()

    def test_tmp(self):
        ### duration settings
        TODAY    = datetime.datetime.now()
        DIFF     = datetime.timedelta(days = 60)
        STARTDAY = TODAY - DIFF

        TODAY_formated    = str(TODAY.year) + "-" + str(TODAY.month) + "-" + str(TODAY.day)
        STARTDAY_formated = str(STARTDAY.year) + "-" + str(STARTDAY.month) + "-" + str(STARTDAY.day)

        stock = YFetcher('3036.TW', STARTDAY_formated, TODAY_formated)



# set testsuit
testcase = ['test_GenTangledMAImg']
suite = unittest.TestSuite(map(APITestCase, testcase))

# start test
unittest.main(verbosity=2)