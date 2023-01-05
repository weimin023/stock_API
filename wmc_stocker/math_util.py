import pandas as pd
from numbers import Number
from typing import Sequence


def SMA(arr: pd.Series, win: int) -> pd.Series:
    '''
    python 3.6 declaration type
    Simple moving average
    '''
    return pd.Series(arr).rolling(win).mean()

def crossover(series1: Sequence, series2: Sequence) -> bool:
    series1 = (
        series1.values if isinstance(series1, pd.Series) else
        (series1, series1) if isinstance(series1, Number) else
        series1)
    series2 = (
        series2.values if isinstance(series2, pd.Series) else
        (series2, series2) if isinstance(series2, Number) else
        series2)
    try:
        return series1[-2] < series2[-2] and series1[-1] > series2[-1]
    except IndexError:
        return False