# 导入backtrader框架
import backtrader as bt
from feed.feedstock import get_stock_history
from strategy.logstrategy import *

cerebro = bt.Cerebro()  # 创建Cerebro引擎
cerebro.addstrategy(TestStrategy, maperiod=20, exitbars=5)  # 为Cerebro引擎添加策略
cerebro.adddata(get_stock_history())  # 加载交易数据
cerebro.broker.setcash(100000.0)  # 设置投资金额100000.0
# 每笔交易使用固定交易量
cerebro.addsizer(bt.sizers.FixedSize, stake=10)
# 设置佣金为0.0

cerebro.broker.setcommission(commission=0.0)
# 引擎运行前打印期出资金
# print("组合期初资金: %.2f" % cerebro.broker.getvalue())
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="mysharpe")
thestrats = cerebro.run(maxcpus=1)
print("夏普比率:", thestrats[0].analyzers.mysharpe.get_analysis())

# cerebro.plot(style="candlestick")
