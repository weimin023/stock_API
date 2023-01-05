import pandas as pd

import bokeh
from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.io import output_file, show
from bokeh.resources import INLINE

from screeninfo import get_monitors


print ("Bokeh Version: {}".format(bokeh.__version__))
curdoc().theme = 'dark_minimal'

apple_df = pd.read_csv('./csv/AAPL.csv', index_col=0, parse_dates=True)
dt_range = pd.date_range(start="2021-12-01", end="2022-10-31")
apple_df = apple_df[apple_df.index.isin(dt_range)]
print (apple_df)

# green LONG, red SHORT
DEFAULT_COLOR = 1
if DEFAULT_COLOR:
    LONG  = "#7FFF00"
    SHORT = "#FF0000"
else:
    LONG  = "#FF0000"
    SHORT = "#7FFF00"

for m in get_monitors():
    if m.is_primary:
        SCREEN_WIDTH  = int(m.width*0.9)
        SCREEN_HEIGHT = int(m.height*0.6)
        break

output_file("../log_lines.html")

inc = apple_df.Close > apple_df.Open
dec = apple_df.Open  > apple_df.Close

W = 12*60*60*1000

## Candlestick Chart
candlestick = figure(x_axis_type = "datetime", width = SCREEN_WIDTH, height = SCREEN_HEIGHT, title = "APPLE", 
                     tools = ['hover, box_select, reset, wheel_zoom, pan, crosshair'], active_scroll = "wheel_zoom")

candlestick.segment(apple_df.index[inc], apple_df.High[inc], apple_df.index[inc], apple_df.Low[inc], color = LONG)
candlestick.segment(apple_df.index[dec], apple_df.High[dec], apple_df.index[dec], apple_df.Low[dec], color = SHORT)

candlestick.vbar(apple_df.index[inc], W, apple_df.Open[inc], apple_df.Close[inc], fill_color = LONG, line_color = LONG)
candlestick.vbar(apple_df.index[dec], W, apple_df.Open[dec], apple_df.Close[dec], fill_color = SHORT, line_color = SHORT)

## Volume Chart
volume = figure(x_axis_type = "datetime", width = SCREEN_WIDTH, height = int(SCREEN_HEIGHT*0.4), x_range = candlestick.x_range, active_scroll = "wheel_zoom")

volume.vbar(apple_df.index[inc], width = W, top = apple_df.Volume[inc]/1e4, fill_color = LONG, line_color = LONG, alpha = 0.8)
volume.vbar(apple_df.index[dec], width = W, top = apple_df.Volume[dec]/1e4, fill_color = SHORT, line_color = SHORT, alpha = 0.8)

volume.xaxis.axis_label = "Date in March"
volume.yaxis.axis_label = "Volume (w)"
candlestick.yaxis.axis_label = "Price (USD)"

show(column(candlestick, volume))