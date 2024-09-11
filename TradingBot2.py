import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from backtesting import Backtest, Strategy

S = "2023-05-01"
E = "2024-05-01"

MSFT = yf.download("MSFT", start= S, end= E, interval='1d')

print(MSFT.head(3))
 
print(MSFT.info())

def MovingAvgCrossOver(data):

    # 3 Day moving AVG
    data["3dayMA"] = data["Close"].rolling(window = 3).mean()

    # 14 Day moving AVG
    data["14dayMA"] = data["Close"].rolling(window = 14).mean()

    # Generate buy/sell signals
    data['Signal'] = 0
    data.loc[data['3dayMA'] > data['14dayMA'], 'Signal'] = 1
    data.loc[data['3dayMA'] < data['14dayMA'], 'Signal'] = -1
    
    class SMA(Strategy):

        def init(self):
            pass

        def next(self):
            current_signal = self.data.Signal[-1]

            if current_signal == 1:
                if not self.position:
                    self.buy()
            elif current_signal == -1:
                if self.position:
                    self.position.close()

    bt = Backtest(data, SMA, cash=10000, commission=.002, exclusive_orders=True)

    stats = bt.run()
    bt.plot()
    print(stats)

def BreakoutUp(data):

    data["14dayMA"] = data["Close"].rolling(window = 14).mean()
    data["14daySD"] = data["Close"].rolling(window = 14).std()
    data["30daySD"] = data["Close"].rolling(window = 30).std()
    
    # Generate buy/sell signals
    data["Signal"] = 0
    data["SignalC"] = 0

    data.loc[data["14daySD"] < 0.5 * data["30daySD"], "SignalC"] = 1

    data.loc[data["Close"] > data["14dayMA"] + 0.2 * data["14daySD"], "Signal"] = 1
    data.loc[data["Close"] < data["Close"].shift(-1), "Signal"] = -1

    class Break(Strategy):

        def init(self):
            pass

        def next(self):
            current_signal = self.data.Signal[-1]
            c_signal = self.data.SignalC[-1]

            if current_signal == 1 & c_signal == 1:
                if not self.position:
                    self.buy()
            elif current_signal == -1:
                    self.position.close()

    bt = Backtest(data, Break, cash=10000, commission=.002, exclusive_orders=True)
    stats = bt.run()
    bt.plot()
    print(stats)

def BreakoutDown(data):

    data["14dayMA"] = data["Close"].rolling(window = 14).mean()
    data["14daySD"] = data["Close"].rolling(window = 14).std()
    data["30daySD"] = data["Close"].rolling(window = 30).std()
    
    # Generate buy/sell signals
    data["Signal"] = 0
    data["SignalC"] = 0

    data.loc[data["14daySD"] < 0.5 * data["30daySD"], "SignalC"] = 1

    data.loc[data["Close"] < data["14dayMA"] - 0.2 * data["14daySD"], "Signal"] = -1
    data.loc[data["Close"] > data["Close"].shift(-1), "Signal"] = 1

    class Break(Strategy):

        def init(self):
            pass

        def next(self):
            current_signal = self.data.Signal[-1]
            c_signal = self.data.SignalC[-1]

            if current_signal == -1 & c_signal == 1:
                if not self.position:
                    self.sell()
            elif current_signal == 1:
                    self.position.close()

    bt = Backtest(data, Break, cash=10000, commission=.002, exclusive_orders=True)
    stats = bt.run()
    bt.plot()
    print(stats)

def MeanReversionBuy(data):

   # 14 Day moving AVG
    data["14dayMA"] = data["Close"].rolling(window = 14).mean()
    data["14daySD"] = data["Close"].rolling(window = 14).std()
    
    Z = 15
    W = Z /10
    # Generate buy/sell signals
    data["Signal"] = 0
    data.loc[data["Close"] > data["14dayMA"] + W * data["14daySD"], "Signal"] = -1
    data.loc[data["Close"] < data["14dayMA"] , "Signal"] = 1

    class MR(Strategy):

        def init(self):
            pass

        def next(self):
            current_signal = self.data.Signal[-1]

            if current_signal == 1:
                if not self.position:
                    self.buy()
            elif current_signal == -1 :
                    self.position.close()

    bt = Backtest(data, MR, cash=10000, commission=.002, exclusive_orders=True)
    stats = bt.run()
    bt.plot()
    print(stats)
    print(data)

    opt = bt.optimize(W = range(5,20,1), maximize = "Return [%]")
    print(opt)

def MeanReversionSell(data):
   # 14 Day moving AVG
    data["14dayMA"] = data["Close"].rolling(window = 14).mean()
    data["14daySD"] = data["Close"].rolling(window = 14).std()

    # Generate buy/sell signals
    data["Signal"] = 0
    data.loc[data["Close"] < data["14dayMA"] - 1.5 * data["14daySD"], "Signal"] = -1
    data.loc[data["Close"] > data["14dayMA"] , "Signal"] = 1

    class MR(Strategy):

        def init(self):
            pass

        def next(self):
            current_signal = self.data.Signal[-1]

            if current_signal == -1:
                if not self.position:
                    self.sell()
            elif current_signal == 1 :
                    self.position.close()

    bt = Backtest(data, MR, cash=10000, commission=.002, exclusive_orders=True)
    stats = bt.run()
    bt.plot()
    print(stats)

def TrendFollowing(data):
    
    data["100dayMA"] = data["Close"].rolling(window = 100).mean()
    data["7dayMA"] = data["Close"].rolling(window = 7).mean()

    # Generate buy/sell signals
    data["Signal"] = 0
    data.loc[(data["Close"] > data["100dayMA"]) & (data['Close'] > data['7dayMA']) , "Signal"] = 1
    data.loc[(data["Close"] > data["100dayMA"]) & (data['Close'] <= data['7dayMA']) , "Signal"] = 0
    data.loc[(data["Close"] < data["7dayMA"]) & (data['Close'] < data['7dayMA']), "Signal"] = -1
    data.loc[(data["Close"] < data["7dayMA"]) & (data['Close'] >= data['7dayMA']), "Signal"] = -1

    class Trend(Strategy):

        def init(self):
            pass

        def next(self):
            current_signal = self.data.Signal[-1]

            if current_signal == 1:
                if not self.position:
                    self.buy()
                elif self.position.is_short:
                    self.position.close()
                    self.buy()
            
            elif current_signal == 0:
                self.position.close()

            elif current_signal == -1:
                if not self.position:
                    self.position.close()
                    self.sell()

    bt = Backtest(data, Trend, cash=10000, commission=.002, exclusive_orders=True)
    stats = bt.run()
    bt.plot()
    print(stats)
            

TrendFollowing(MSFT)

#MeanReversionSell(GOOG)
#MeanReversionBuy(MSFT)
#MovingAvgCrossOver(MSFT)
#BreakoutDown(GOOG) 
#BreakoutUp(GOOG) 

