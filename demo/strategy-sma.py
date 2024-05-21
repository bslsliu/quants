import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
 
#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False
 
#引入TA-Lib库
import talib as ta
import time
from datetime import datetime, timedelta
# import tushare as ts
# df=ts.get_k_data('sh',start='2000-01-01')
# df.index=pd.to_datetime(df.date)
# df=df.sort_index()
# df['ret']=df.close/df.close.shift(1)-1
# df.head()
import akshare as ak

df = ak.stock_zh_a_hist(symbol="000001", adjust="hfq").iloc[:, :6]
    # 处理字段命名，以符合 Backtrader 的要求
df.columns = [
    'date',
    'open',
    'close',
    'high',
    'low',
    'volume',
    ]
df.index=pd.to_datetime(df.date)
df=df.sort_index()
df['ret']=df.close/df.close.shift(1)-1
df['fast_sma'] = ta.SMA(df['close'],timeperiod=5)
df['slow_sma'] = ta.SMA(df['close'],timeperiod=20)
df.dropna()
df_new = df.loc['2020-01-01':'2024-05-20'].copy() 
df_new['pos']=0
df_new['pos'][df_new['fast_sma']>df_new['slow_sma']] = 1
df_new['pos'][df_new['fast_sma']<=df_new['slow_sma']] = 0 
df_new['pos'] = df_new['pos'].shift(1).fillna(0)
df_new['pos'].ffill(inplace=True)
df_new['equity']=(df_new['ret']*df_new['pos']+1).cumprod() 

df_new['equity']