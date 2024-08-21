#导入backtrader框架  
import backtrader as bt 
from feedstock import get_stock_history

# 创建策略继承bt.Strategy 
class TestStrategy(bt.Strategy): 

    def log(self, txt, dt=None): 
        # 记录策略的执行日志  
        dt = dt or self.datas[0].datetime.date(0) 
        print('%s, %s' % (dt.isoformat(), txt)) 

    def __init__(self): 
        # 保存收盘价的引用  
        self.dataclose = self.datas[0].close 

    def next(self): 
        # 记录收盘价  
        self.log('Close, %.2f' % self.dataclose[0]) 
        
# 创建Cerebro引擎  
cerebro = bt.Cerebro() 
# Cerebro引擎在后台创建broker(经纪人)，系统默认资金量为10000 
# 为Cerebro引擎添加策略  
cerebro.addstrategy(TestStrategy) 

data = get_stock_history() # 加载交易数据  

cerebro.adddata(data)
# 设置投资金额100000.0 
cerebro.broker.setcash(100000.0) 
# 引擎运行前打印期出资金  
print('组合期初资金: %.2f' % cerebro.broker.getvalue()) 
cerebro.run() 
# 引擎运行后打期末资金  
print('组合期末资金: %.2f' % cerebro.broker.getvalue())