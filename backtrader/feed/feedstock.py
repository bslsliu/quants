import datetime
import pandas as pd
import backtrader as bt
from datetime import datetime
import akshare as ak


def get_stock_history():
    stock_hfq_df = ak.stock_zh_a_hist(symbol="000001", adjust="hfq").iloc[:, :6]
    # 处理字段命名，以符合 Backtrader 的要求
    stock_hfq_df.columns = [
        "date",
        "open",
        "close",
        "high",
        "low",
        "volume",
    ]
    # 把 date 作为日期索引，以符合 Backtrader 的要求
    stock_hfq_df.index = pd.to_datetime(stock_hfq_df["date"])
    start_date = datetime(2024, 1, 1)  # 回测开始时间
    end_date = datetime(2024, 4, 15)  # 回测结束时间
    data = bt.feeds.PandasData(
        dataname=stock_hfq_df, fromdate=start_date, todate=end_date
    )  # 加载数据
    return data


def get_stock_by_csv():
    params = dict(
        fromdate=datetime.datetime(2010, 1, 1), todate=datetime.datetime(2020, 3, 21)
    )
    df.columns = ["datetime", "open", "close", "high", "low", "volume", "openinterest"]
    df.index = pd.to_datetime(df["datetime"])
    df = df[["open", "high", "low", "close", "volume", "openinterest"]]
    feed = bt.feeds.PandasDirectData(dataname=df, **params)
    return feed
