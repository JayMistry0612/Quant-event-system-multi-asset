class event:
    pass

class MarketEvent(event):
    def __init__(self,data):
        self.type = 'MARKET'
        self.data = data

class SignalEvent(event):
    def __init__(self,signal,data):
        self.type = 'SIGNAL'
        self.signal=signal   
        self.data=data

class OrderEvent(event):
    def __init__(self,signal,price):
        self.type = 'ORDER'
        self.signal = signal
        self.price = price   