import yfinance as yf
# import seaborn as sns
from screeninfo import get_monitors

from wmc_stocker.math_util import *

import pandas as pd

from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.io import output_file, show, export_png, export_svgs
from bokeh.resources import INLINE
from bokeh.models import Arrow, CDSView, BooleanFilter, NormalHead, OpenHead, VeeHead, Label, Legend, HoverTool, ColumnDataSource

import os

DEBUG_MODE = 1

class Fetcher:
    def __init__(self):
        pass
    def Plot(self): #virtual function.
       raise NotImplementedError( "Plot is virutal! Must be overwrited." )


class YFetcher(Fetcher):
    # constructor
    # | ex: "SPY AAPL", start="2017-01-01", end="2017-04-30"
    def __init__(self, STOCKID, STARTD, ENDD):
        self.__STOCKID = STOCKID
        self.__STARTD  = STARTD
        self.__ENDD    = ENDD

    def Fetch(self):
        self.__DATA_ = yf.download(self.__STOCKID, self.__STARTD, self.__ENDD, progress=False)
        # print (self.__DATA_.empty)
        return self.__DATA_

    def GetName(self):
        return self.__STOCKID
    '''
    def BuyIndicator(self, fig: figure, x, y, ArrorColor = "aqua", LineColor = "lightcyan"):
        return fig.add_layout(Arrow(end=VeeHead(line_color = LineColor, line_width=3, fill_color = ArrorColor),
                       line_color = LineColor, line_width = 2,
                       x_start = x, y_start = y + 0.5,
                       x_end = x, y_end = y + 0.7))
    
    
    def SellIndicator(self, fig: figure, x, y, ArrorColor = "deeppink", LineColor = "pink"):
        return fig.add_layout(Arrow(end=VeeHead(line_color = LineColor, line_width=3, fill_color = ArrorColor),
                       line_color = LineColor, line_width = 2,
                       x_start = x, y_start = y - 0.5,
                       x_end = x, y_end = y - 0.7))
    '''

class Plotter:
    def __init__(self, data: pd.DataFrame, stockID:str, DEFAULT_COLOR = 1):
        self.__DEFAULT_COLOR = DEFAULT_COLOR
        self.__DATA_         = data
        self.__stockID       = stockID

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
        
        # Candlestick Chart
        self._candlestick = figure(x_axis_type = "datetime",
                            width = self.__SCREEN_WIDTH, height = self.__SCREEN_HEIGHT,
                            title = self.__stockID, 
                            tools = ['box_select, reset, wheel_zoom, pan, crosshair'],
                            active_scroll = "wheel_zoom")

    def BuyIndicator(self, fig: figure, x, y, size = 20, marker = "triangle"):
        return fig.scatter(x, y+0.5, size = size, marker = marker, fill_color="aquamarine")

    
    def SellIndicator(self, fig: figure, x, y, size = 20, marker = "inverted_triangle"):
        return fig.scatter(x, y-0.5, size = size, marker = marker, fill_color="hotpink")

    def GetFig(self):
        return self._candlestick

    def GetPlot(self):

        # plot candlestick        
        __inc = self.__DATA_.Close > self.__DATA_.Open
        __dec = self.__DATA_.Open  > self.__DATA_.Close
        __W = 12*60*60*1000

        df = self.__DATA_
        
        df['openinc']  = df.Open[__inc]
        df['closeinc'] = df.Close[__inc]

        df['opendec']  = df.Open[__dec]
        df['closedec'] = df.Close[__dec]

        df['date']     = df.index.values

        df['highinc']  = df.High[__inc]
        df['lowinc']   = df.Low[__inc]

        df['highdec']  = df.High[__dec]
        df['lowdec']   = df.Low[__dec]

        source = ColumnDataSource(df)

        # Candlestick Chart
        candlestick = self._candlestick

        candlestick.segment('Date', 'highinc',
                            'Date', 'lowinc', color = self.__LONG, source = source)

        candlestick.segment('Date', 'highdec',
                            'Date', 'lowdec', color = self.__SHORT, source = source)
        
        up   = candlestick.vbar('date', __W, 'openinc', 'closeinc',
                        fill_color = self.__LONG, line_color = self.__LONG, source = source)
        
        down = candlestick.vbar('date', __W, 'opendec', 'closedec',
                        fill_color = self.__SHORT, line_color = self.__SHORT, source = source)
        
        hover_tool = HoverTool(tooltips = [
                                    ('date', '@date{%F}'),
                                    ('High',"@High{0.2f}"),
                                    ('Low',"@Low{0.2f}"),
                                    ('Open','@Open{0.2f}'),
                                    ('Close',"@Close{0.2f}"),
                                ],
                                formatters = {
                                    "@date": 'datetime',
                                },
                                mode = 'mouse'
                            )

        candlestick.add_tools(hover_tool)

        # Plot MA
        self.ma1 = SMA(df.Close, 5)
        self.ma2 = SMA(df.Close, 10)
        self.ma3 = SMA(df.Close, 20)

        ma5  = candlestick.line(df.index.values, self.ma1, color = 'gold', line_width = 1)
        ma10 = candlestick.line(df.index.values, self.ma2, color = 'darkviolet', line_width = 1)
        ma20 = candlestick.line(df.index.values, self.ma3, color = 'fuchsia', line_width = 1)

        # legend settings
        legend = Legend(items=[
            ("Up",   [up]),
            ("Down", [down]),
            ("MA5",  [ma5]),
            ("MA10", [ma10]),
            ("MA20", [ma20])
        ], location=(0, -5))

        candlestick.add_layout(legend)

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

        volume.xaxis.axis_label = "日期"
        volume.yaxis.axis_label = "成交量 (萬)"
        candlestick.yaxis.axis_label = "市價 (NTD)"

        if not DEBUG_MODE:
            show(column(candlestick, volume))

        if DEBUG_MODE:
            # Save figure to file
            # output_file("./log.png")
            fpath  = os.getcwd() + "\debug\\"
            fname = self.__stockID
            if not os.path.exists(os.path.join(os.getcwd(), 'debug')): 
                os.mkdir(fpath)
                print (fpath, " directory is created!" )
            export_png(candlestick, filename = fpath + fname + ".png")