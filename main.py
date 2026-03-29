import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.data_handler import DataHandler
from src.strategy import Strategy
from src.event_queue import EventQueue
from src.events import MarketEvent,SignalEvent,OrderEvent
from src.portfolio import Portfolio
from src.event_queue import EventQueue
from src.execution import Execution
from src.metrics import Metrics


data={
    'RELIANCE':pd.read_parquet('data/RELIANCE.parquet')
    ,'LT':pd.read_parquet('data/LT.parquet')
    ,'HDFCBANK':pd.read_parquet('data/HDFCBANK.parquet')
}

queue=EventQueue()
data_handler=DataHandler(data)
strategy=Strategy()
portfolio=Portfolio()
execution=Execution()

last_data = {}

while True:
    batch = data_handler.stream_next()
    if batch is None:
        break
    for symbol,row in batch.items():
        last_data[symbol]=row
        queue.put(MarketEvent(row,symbol))
    
    while not queue.is_empty():
        event = queue.get()
        
        if event.type=='MARKET':
            signal=strategy.on_market(event.data,event.symbol)
            
            if signal:
                queue.put(SignalEvent(signal,event.data,event.symbol))
                        
        elif event.type=='SIGNAL':
            signal,price=execution.execute(event.signal,event.data)
            queue.put(OrderEvent(signal,price,event.symbol))
        
        elif event.type=='ORDER':
            portfolio.update(event.signal,event.symbol,event.price)
          
        portfolio.mark_to_market(batch)    
            
for symbol in list(portfolio.positions.keys()):
    last_price = last_data[symbol]['Close']
    portfolio.update('SELL', symbol, last_price)

metrics = Metrics(portfolio.profit_curve, portfolio.equity_curve)
print('Sharpe Ratio:', metrics.sharpe_ratio())
print('Max Drawdown:', metrics.max_drawdown())
print("Total trades:",len(portfolio.profit_curve))                        
print("Total profit:",sum(portfolio.profit_curve))
print("Average Profit:",np.mean(portfolio.profit_curve))
print('Win Rate:', metrics.win_rate())



plt.figure(figsize=(12,6))
plt.subplot(2,1,1)
plt.plot(portfolio.equity_curve,label='Equity Curve')
plt.title('Equity Curve')   

plt.subplot(2,1,2)
plt.plot(portfolio.profit_curve,label='Profit Curve')
plt.title('Profit Curve')
plt.tight_layout()
plt.show()