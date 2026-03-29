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


data=pd.read_parquet('data/lt_data.parquet')

queue=EventQueue()
data_handler=DataHandler(data)
strategy=Strategy()
portfolio=Portfolio()
execution=Execution()

while True:
    row = data_handler.stream_next()
    if row is None:
        break
    queue.put(MarketEvent(row))
    
    while not queue.is_empty():
        event = queue.get()
        
        if event.type=='MARKET':
            signal=strategy.on_market(event.data)
            
            if signal:
                queue.put(SignalEvent(signal,event.data))
            
            portfolio.mark_to_market(event.data['Close'])
            
        elif event.type=='SIGNAL':
            signal,price=execution.execute(event.signal,event.data)
            queue.put(OrderEvent(signal,price))
        
        elif event.type=='ORDER':
            portfolio.update(event.signal,event.price)
if portfolio.position!=0:
    portfolio.update('SELL',data_handler.current_row['Close'])

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