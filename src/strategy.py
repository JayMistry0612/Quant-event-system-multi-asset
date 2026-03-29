class Strategy:
    def __init__(self):
        self.prev = {}
        

    def on_market(self, data,symbol):

        if symbol not in self.prev:
            self.prev[symbol] = data
            return None

        prev=self.prev[symbol]
        
        tolerance = 0.005
        threshold = 0.001
        
        ema_20 = prev['EMA_20']
        ema_50 = prev['EMA_50']
        price = prev['Close']
        
        
        strength = abs(prev['EMA_20'] - prev['EMA_50']) / prev['Close']
        
        if strength < threshold:
            self.prev[symbol] = data
            return None
        
        if ema_20 > ema_50 and price <= ema_20 * (1 + tolerance) and price >= ema_20 * (1 - tolerance):
            signal = 'BUY'
        elif ema_20 < ema_50 and price >= ema_20 * (1 - tolerance) and price <= ema_20 * (1 + tolerance):
            signal = 'SELL'
        else:
            signal = None    
        
        self.prev[symbol] = data

        return signal