import yfinance as yf
import seaborn as sns

import mplfinance as mpf
# import matplotlib.pyplot as plt

import pandas as pd

import bokeh
from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.io import output_file, show
from bokeh.resources import INLINE

from screeninfo import get_monitors

class Fetcher:
    def __init__(self):
        pass
    def Plot(self): #virtual function.
       raise NotImplementedError( "Plot is virutal! Must be overwrited." )


class YFetcher(Fetcher):
    # constructor
    # | ex: "SPY AAPL", start="2017-01-01", end="2017-04-30"
    def __init__(self, STOCKID, STARTD, ENDD, DEFAULT_COLOR = 1):
        self.__STOCKID = STOCKID
        self.__STARTD  = STARTD
        self.__ENDD    = ENDD
        self.__DEFAULT_COLOR = DEFAULT_COLOR

        ### ENV SETTING
        # COLOR
        if self.__DEFAULT_COLOR:
            self.__LONG  = "#7FFF00"
            self.__SHORT = "#FF0000"
        else:
            self.__LONG  = "#FF0000"
            self.__SHORT = "#7FFF00"

        # THEME
        curdoc().theme = 'dark_minimal'

        # DISPLAY INFO
        for m in get_monitors():
            if m.is_primary:
                self.__SCREEN_WIDTH  = int(m.width*0.9)
                self.__SCREEN_HEIGHT = int(m.height*0.6)
                break

    def Fetch(self):
        self.__DATA_ = yf.download(self.__STOCKID, self.__STARTD, self.__ENDD)
        return self.__DATA_

    def Plot(self, indicator: pd.DataFrame):
        # print (indicator['Idx'])
        # plot candlestick
        # fig, axes = mpf.plot(self.__DATA_, type = 'candle', mav = (3,6,9), volume = True, show_nontrading = True, style = 'binance')

        __inc = self.__DATA_.Close > self.__DATA_.Open
        __dec = self.__DATA_.Open  > self.__DATA_.Close
        print (self.__DATA_.loc[indicator['Date']])
        __W = 12*60*60*1000

        # Candlestick Chart
        candlestick = figure(x_axis_type = "datetime",
                            width = self.__SCREEN_WIDTH, height = self.__SCREEN_HEIGHT,
                            title = self.__STOCKID, 
                            tools = ['hover, box_select, reset, wheel_zoom, pan, crosshair'],
                            active_scroll = "wheel_zoom")

        candlestick.segment(self.__DATA_.index[__inc], self.__DATA_.High[__inc],
                            self.__DATA_.index[__inc], self.__DATA_.Low[__inc], color = self.__LONG)

        candlestick.segment(self.__DATA_.index[__dec], self.__DATA_.High[__dec],
                            self.__DATA_.index[__dec], self.__DATA_.Low[__dec], color = self.__SHORT)

        candlestick.vbar(self.__DATA_.index[__inc], __W, self.__DATA_.Open[__inc], self.__DATA_.Close[__inc],
                        fill_color = self.__LONG, line_color = self.__LONG)

        candlestick.vbar(self.__DATA_.index[__dec], __W, self.__DATA_.Open[__dec], self.__DATA_.Close[__dec],
                        fill_color = self.__SHORT, line_color = self.__SHORT)

        # (TODO) Plot indicators
        
        # Volume Chart
        volume = figure(x_axis_type = "datetime",
                        width = self.__SCREEN_WIDTH, height = int(self.__SCREEN_HEIGHT*0.4),
                        x_range = candlestick.x_range, active_scroll = "wheel_zoom")

        volume.vbar(self.__DATA_.index[__inc],
                    width = __W,
                    top = self.__DATA_.Volume[__inc]/1e4,
                    fill_color = self.__LONG, line_color = self.__LONG, alpha = 0.8)

        volume.vbar(self.__DATA_.index[__dec],
                    width = __W,
                    top = self.__DATA_.Volume[__dec]/1e4,
                    fill_color = self.__SHORT, line_color = self.__SHORT, alpha = 0.8)

        volume.xaxis.axis_label = "Date"
        volume.yaxis.axis_label = "Volume (w)"
        candlestick.yaxis.axis_label = "Price (USD)"

        show(column(candlestick, volume))

        # Save figure to file
        # output_file("./log_lines.html")
        


'''
stock = YFetcher("0050.TW", "2021-01-01", "2022-10-31")
stock.Fetch()
stock.Plot()
'''