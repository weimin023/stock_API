from wmc_stocker.def_strategy import *
from wmc_stocker.top_backtest import *
from wmc_stocker.util import *

import datetime, csv, time
import pandas as pd
import multiprocessing as mp

import sqlite3

fPATH = ".\stock_pool\stock_list_csv.csv"
### duration settings
TODAY    = datetime.datetime.now()
DIFF     = datetime.timedelta(days = 60)
STARTDAY = TODAY - DIFF

TODAY_formated    = str(TODAY.year) + "-" + str(TODAY.month) + "-" + str(TODAY.day)
STARTDAY_formated = str(STARTDAY.year) + "-" + str(STARTDAY.month) + "-" + str(STARTDAY.day)

def func(data: pd.DataFrame)->list:
    DELIST = []
    for row in data.itertuples(index=True):
        stock = YFetcher(row.symbol, STARTDAY_formated, TODAY_formated)
        df = stock.Fetch()
        
        if df.empty:
            DELIST.append(row.Index)
    return DELIST

def Save2DB(data: pd.DataFrame):
    # create a database
    con = sqlite3.connect(".\stock_pool\stock_pool.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE stock_pool(symbol,name,status,category)")
    con.commit()

    # write into database
    data.to_sql('stock_pool', con, if_exists='append', index=False)
    # con.close()

def DailyReflashPool()->None:
    ### load symbol pool
    csv_ = pd.read_csv(fPATH)
    RNUM = csv_.shape[0]

    # create as many processes as there are CPUs on your machine
    num_processes = mp.cpu_count()-1

    # calculate the chunk size as an integer
    chunk_size = 50

    # this solution was reworked from the above link.
    # will work even if the length of the dataframe is not evenly divisible by num_processes
    chunks = np.array_split(csv_, chunk_size)
    
    # create our pool with `num_processes` processes
    pool = mp.Pool(processes=num_processes)

    start = time.time()

    # apply our function to each chunk in the list
    DELIST = []
    result = pool.map(func, chunks)
    pool.close()
    pool.join()

    end = time.time()

    for i in result:
        DELIST.extend(i)

    print ("total time: ", end-start)
    print ("DELIST: ", DELIST)

    # delist invalid symbols
    LIST_ = [i for i in range(RNUM) if i not in DELIST]
    csv_ = csv_.iloc[LIST_]
    #csv_.to_csv(fPATH, index=False, encoding="utf_8_sig")

    Save2DB(csv_)

if __name__ == '__main__':
    # DailyReflashPool()
    NotImplemented

    

'''
    DELIST = []
    for row in csv_.itertuples(index=True):
        #stock = YFetcher("^TWII", STARTDAY_formated, TODAY_formated)
        stock = YFetcher(row.symbol, STARTDAY_formated, TODAY_formated)

        # stock.Plot()
        df = stock.Fetch()
        
        if df.empty:
            DELIST.append(row.Index)
            #print (row.symbol, row.name)

    LIST_ = [i for i in range(RNUM) if i not in DELIST]
    csv_ = csv_.iloc[LIST_]
    csv_.to_csv(fPATH, index=False, encoding="utf_8_sig")'''

    # backtest
    #bt = Backtest(stock, LongArrangement, cash=50000, commission=.002)
    #print (bt.run())
    #bt.plot()






'''
import sqlite3

# create a database
con = sqlite3.connect("stock_history.db")
cur = con.cursor()
# cur.execute("CREATE TABLE history_data(Date, Open, High, Low, Close, Volume)")
con.commit()

# write into database
df = df.drop(columns=['Adj Close'])
df.to_sql('history_data', con, if_exists='append', index=True)
# con.close()

us_df = pd.read_sql("SELECT * FROM history_data", con)
print (us_df)



'''
