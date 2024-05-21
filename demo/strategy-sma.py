#!/usr/bin/env python
# coding: utf-8
#先引入后面可能用到的包（package）
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
df['fast_sma'] = df['close'].rolling(50).mean()
df['slow_sma'] = df['close'].rolling(200).mean()

df['pos']=0
df['pos'][df['ma5']>=df['ma20']] = 1
df['pos'][df['ma5']<df['ma20']] = -1 #做空
df['pos'] = df['pos'].shift(1).fillna(0)

df.index=pd.to_datetime(df.date)
df=df.sort_index()
df['ret']=df.close/df.close.shift(1)-1
 
 
high,low,close,volume=df.high.values,df.low.values,df.close.values,df.volume.values
df['mfi']=ta.MFI(high, low, close, volume, timeperiod=14)
plt.figure(figsize=(16,14))
plt.subplot(211)
df['close'].plot(color='r')
plt.xlabel('')
plt.title('上证综指走势',fontsize=15)
plt.subplot(212)
df['mfi'].plot()
plt.title('MFI指标',fontsize=15)
plt.xlabel('')
plt.show()
 
 
#当前日的MFI<20，而当日的MFI>20时，买入信号设置为1
for i in range(15,len(df)):
    if df['mfi'][i]>20 and df['mfi'][i-1]<20:
        df.loc[df.index[i],'收盘信号']=1
    if df['mfi'][i]<80 and df['mfi'][i-1]>80:
        df.loc[df.index[i],'收盘信号']=0
 
 
#计算每天的仓位，当天持有上证指数时，仓位为1，当天不持有上证指数时，仓位为0
pd.options.mode.chained_assignment = None
df['当天仓位']=df['收盘信号'].shift(1)
df['当天仓位'].fillna(method='ffill',inplace=True)
 
 
from datetime import datetime,timedelta
d=df[df['当天仓位']==1].index[0]-timedelta(days=1)
df_new=df.loc[d:]
df_new['ret'][0]=0
df_new['当天仓位'][0]=0
 
 
#当仓位为1时，买入上证指数，当仓位为0时，空仓，计算资金指数
df_new['资金指数']=(df_new.ret*df['当天仓位']+1.0).cumprod()
df_new['指数净值']=(df_new.ret+1.0).cumprod()
 
 
df.close.plot(figsize=(16,7))
for i in range(len(df)):
    if df['收盘信号'][i]==1:
        plt.annotate('买',xy=(df.index[i],df.close[i]),arrowprops=dict(facecolor='r',shrink=0.05))
    if df['收盘信号'][i]==0:
        plt.annotate('卖',xy=(df.index[i],df.close[i]),arrowprops=dict(facecolor='g',shrink=0.1))    
plt.title('上证指数2000-2019年MFI买卖信号',size=15)
plt.xlabel('')
ax=plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.show()
 
 
#查看最近两年情况
df1=df.loc['2016-01-01':,]
df1.close.plot(figsize=(16,7))
for i in range(len(df1)):
    if df1['收盘信号'][i]==1:
        plt.annotate('买',xy=(df1.index[i],df1.close[i]),arrowprops=dict(facecolor='r',shrink=0.05))
    if df1['收盘信号'][i]==0:
        plt.annotate('卖',xy=(df1.index[i],df1.close[i]),arrowprops=dict(facecolor='g',shrink=0.1))    
plt.title('上证指数2016-2019年MFI买卖信号',fontsize=15)
plt.xlabel('')
ax=plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.show()
 
df1['策略净值']=(df1.ret*df1['当天仓位']+1.0).cumprod()
df1['指数净值']=(df1.ret+1.0).cumprod()
 
df1['策略收益率']=df1['策略净值']/df1['策略净值'].shift(1)-1
df1['指数收益率']=df1.ret
total_ret=df1[['策略净值','指数净值']].iloc[-1]-1
annual_ret=pow(1+total_ret,250/len(df_new))-1
dd=(df1[['策略净值','指数净值']].cummax()-df1[['策略净值','指数净值']])/df1[['策略净值','指数净值']].cummax()
d=dd.max()
beta=df1[['策略收益率','指数收益率']].cov().iat[0,1]/df1['指数收益率'].var()
alpha=(annual_ret['策略净值']-annual_ret['指数净值']*beta)
exReturn=df1['策略收益率']-0.03/250
sharper_atio=np.sqrt(len(exReturn))*exReturn.mean()/exReturn.std()
TA1=round(total_ret['策略净值']*100,2)
TA2=round(total_ret['指数净值']*100,2)
AR1=round(annual_ret['策略净值']*100,2)
AR2=round(annual_ret['指数净值']*100,2)
MD1=round(d['策略净值']*100,2)
MD2=round(d['指数净值']*100,2)
S=round(sharper_atio,2)
print(f'累计收益率：策略{TA1}%，指数{TA2}%;\n年化收益率：策略{AR1}%，指数{AR2}%；\n最大回撤：  策略{MD1}%，指数{MD2}%;\n策略alpha: {round(alpha,2)}，策略beta：{round(beta,2)}; \n夏普比率：  {S}')
 
df1[['策略净值','指数净值']].plot(figsize=(15,7))
plt.title('上证指数与MFI指标策略\n2016年1月1日至今',size=15)
 
bbox = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
 
plt.text('2017-05-01', 0.75, f'累计收益率：策略{TA1}%，指数{TA2}%;\n年化收益率：策略{AR1}%，指数{AR2}%；\n最大回撤：  策略{MD1}%，指数{MD2}%;\n策略alpha: {round(alpha,2)}，策略beta：{round(beta,2)}; \n夏普比率：  {S}',         size=13,bbox=bbox)  
plt.xlabel('')
ax=plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.show()