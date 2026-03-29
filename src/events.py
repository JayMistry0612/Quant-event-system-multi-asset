class event:
    pass

class MarketEvent(event):
    def __init__(self,data,symbol):
        self.type = 'MARKET'
        self.data = data
        self.symbol = symbol


class SignalEvent(event):
    def __init__(self,signal,data,symbol):
        self.type = 'SIGNAL'
        self.signal=signal   
        self.data=data
        self.symbol=symbol

class OrderEvent(event):
    def __init__(self,signal,price,symbol):
        self.type = 'ORDER'
        self.signal = signal
        self.price = price
        self.symbol = symbol