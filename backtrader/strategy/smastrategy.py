import backtrader as bt
class SmaStrategy(bt.Strategy):
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
                self.buy(size=1)    
                print(f'Buy Signal At Current Date: {current_date}, buy At {self.datas[0].open[1]}')
        else:
            #执行卖出条件判断：收盘价格跌破20日均线
            if self.crossover < 0:
                # 获取当前日期
                current_date = self.datas[0].datetime.date(0)
                # 执行卖出
                self.close()
                print(f'Sale Signal at Current Date: {current_date}, sale at {self.datas[0].open[1]}')
                # print(self.data)