class Strategy:
    def __init__(self):
        self.prev = {}
        self.prev_prev = {}

    def on_market(self, data,symbol):

        if symbol not in self.prev:
            self.prev[symbol] = data
            return None

        if symbol not in self.prev_prev:
            self.prev_prev[symbol] = self.prev[symbol]
            self.prev[symbol] = data
            return None

        prev=self.prev[symbol]
        prev_prev=self.prev_prev[symbol]
        
        diff1 = prev['EMA_20'] - prev['EMA_50']       
        diff2 = prev_prev['EMA_20'] - prev_prev['EMA_50']  

        if diff1 > 0 and diff2 < 0:
            signal = 'BUY'
        elif diff1 < 0 and diff2 > 0:
            signal = 'SELL'
        else:
            signal = None

        self.prev_prev[symbol] = self.prev[symbol]
        self.prev[symbol] = data

        return signal