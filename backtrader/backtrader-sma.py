import datetime
 
import pandas as pd
 
import backtrader as bt
from datetime import datetime
import matplotlib
import akshare as ak
# %matplotlib inline
 
class SmaCross(bt.Strategy):
 
    # 全局设定交易策略的参数
 
    params = (('pfast', 5), ('pslow', 20),)
 
    def __init__(self):
 
      
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
 
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
 
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
 
    def next(self):
        # 检查是否持仓   
        if not self.position: # 没有持仓
            #执行买入条件判断：收盘价格上涨突破20日均线
            if self.crossover > 0:
                # 获取当前日期
                current_date = self.datas[0].datetime.date(0)
                print('Buy Signal At Current Date: {}'.format(current_date))

                self.buy(size=1)    
                print(self.data)     
        else:
            #执行卖出条件判断：收盘价格跌破20日均线
            if self.crossover < 0:
                # 获取当前日期
                current_date = self.datas[0].datetime.date(0)
                print('Sale Signal at Current Date: {}'.format(current_date))
                #执行卖出
                self.close()
                print("Sale at {} shares".format(self.data.close[0]))
                print(self.data)
             
class MySignal(bt.Indicator):
    lines = ('signal',) # 声明 signal 线，交易信号放在 signal line 上
    params = (('pfast', 5), ('pslow', 20),)

    def __init__(self):
        self.lines.signal = bt.indicators.SMA(period=self.p.pfast)-bt.indicators.SMA(period=self.p.pslow)
 
 
def bt1():
 
    # 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列
    stock_hfq_df = ak.stock_zh_a_hist(symbol="000001", adjust="hfq").iloc[:, :6]
    # 处理字段命名，以符合 Backtrader 的要求
    stock_hfq_df.columns = [
    'date',
    'open',
    'close',
    'high',
    'low',
    'volume',
    ]
    # 把 date 作为日期索引，以符合 Backtrader 的要求
    stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])
    start_date = datetime(2024, 1, 1)  # 回测开始时间
    end_date = datetime(2024, 4, 15)  # 回测结束时间
    data = bt.feeds.PandasData(dataname=stock_hfq_df, 
                           fromdate=start_date, 
                           todate=end_date)  # 加载数据
 
    # 初始化cerebro回测系统设置
 
    cerebro = bt.Cerebro()
 
    # 将数据传入回测系统
 
    cerebro.adddata(data)
 
    # 将交易策略加载到回测系统中
 
    cerebro.addstrategy(SmaCross)
 
    # 设置初始资本为10,000
 
    startcash = 100000

    # cerebro.add_signal(bt.SIGNAL_LONG, MySignal)
 

    cerebro.broker.setcash(startcash)
 
    # 设置交易手续费为 0.1%
 
    # cerebro.broker.setcommission(commission=0.001)
 
    # 运行回测系统
 
    cerebro.run()
 
    # 获取回测结束后的总资金
 
    portvalue = cerebro.broker.getvalue()
 
    pnl = portvalue - startcash

 
    print(f'净收益: {round(pnl,2)}')
 
    # 打印结果
 
    print(f'总资金: {round(portvalue,2)}')


    # print(stock_hfq_df.close[-1])
    # print(stock_hfq_df.close[0])
  
 
    cerebro.plot(style='candlestick')
 
 
if __name__ == '__main__':
    bt1()