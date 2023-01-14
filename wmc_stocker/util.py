import yfinance as yf
# import seaborn as sns
from screeninfo import get_monitors

from wmc_stocker.math_util import *

import pandas as pd

from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.io import output_file, show
from bokeh.resources import INLINE
from bokeh.models import Arrow, CDSView, BooleanFilter, NormalHead, OpenHead, VeeHead, Label, Legend, HoverTool, ColumnDataSource


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

    def BuyIndicator(self, fig: figure, x, y, size = 20, marker = "triangle"):
        return fig.scatter(x, y+0.5, size = size, marker = marker, fill_color="aquamarine")

    
    def SellIndicator(self, fig: figure, x, y, size = 20, marker = "inverted_triangle"):
        return fig.scatter(x, y-0.5, size = size, marker = marker, fill_color="hotpink")


    def Plot(self, indicator: pd.DataFrame):

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
        candlestick = figure(x_axis_type = "datetime",
                            width = self.__SCREEN_WIDTH, height = self.__SCREEN_HEIGHT,
                            title = self.__STOCKID, 
                            tools = ['box_select, reset, wheel_zoom, pan, crosshair'],
                            active_scroll = "wheel_zoom")

        candlestick.segment('Date', 'highinc',
                            'Date', 'lowinc', color = self.__LONG, source = source)

        candlestick.segment('Date', 'highdec',
                            'Date', 'lowdec', color = self.__SHORT, source = source)
        
        candlestick.vbar('date', __W, 'openinc', 'closeinc',
                        fill_color = self.__LONG, line_color = self.__LONG, legend_label = 'Up', source = source)
        
        candlestick.vbar('date', __W, 'opendec', 'closedec',
                        fill_color = self.__SHORT, line_color = self.__SHORT, legend_label = 'Down', source = source)
        
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


        # Plot indicators
        triggeredTradeList = self.__DATA_.loc[indicator['Date']]
        cnt = 0
        for idx, row in triggeredTradeList.iterrows():
            if cnt%2 == 0:
                self.BuyIndicator(candlestick, idx, row['High'])
            else:
                self.SellIndicator(candlestick, idx, row['Low'])
            cnt += 1

        # Plot MA
        self.ma1 = SMA(df.Close, 5)
        self.ma2 = SMA(df.Close, 20)
        self.ma3 = SMA(df.Close, 60)

        candlestick.line(df.index.values, self.ma1, legend_label = 'MA5', color = 'gold', line_width = 1)
        candlestick.line(df.index.values, self.ma2, legend_label = 'MA20', color = 'darkviolet', line_width = 1)
        candlestick.line(df.index.values, self.ma3, legend_label = 'MA60', color = 'fuchsia', line_width = 1)

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