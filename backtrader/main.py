#导入backtrader框架  
import backtrader as bt 
from feed.feedstock import get_stock_history
from strategy.logstrategy import *

cerebro = bt.Cerebro() # 创建Cerebro引擎  
cerebro.addstrategy(TestStrategy) # 为Cerebro引擎添加策略  
cerebro.adddata(get_stock_history()) # 加载交易数据  
cerebro.broker.setcash(100000.0) # 设置投资金额100000.0 
# cerebro.broker.setcommission(commission=0.001) # 设置交易手续费为 0.1%
# 引擎运行前打印期出资金  
print('组合期初资金: %.2f' % cerebro.broker.getvalue()) 
cerebro.run()
# 引擎运行后打期末资金  
print('组合期末资金: %.2f' % cerebro.broker.getvalue())


# cerebro.plot(style='candlestick')
