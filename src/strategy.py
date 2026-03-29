class Strategy:
    def __init__(self):
        self.prev = None
        self.prev_prev = None

    def on_market(self, data):

        # Step 1: if not enough data, just build history
        if self.prev is None:
            self.prev = data
            return None

        if self.prev_prev is None:
            self.prev_prev = self.prev
            self.prev = data
            return None

        # Step 2: generate signal using OLD data
        diff1 = self.prev['EMA_20'] - self.prev['EMA_50']       # t-1
        diff2 = self.prev_prev['EMA_20'] - self.prev_prev['EMA_50']  # t-2

        if diff1 > 0 and diff2 < 0:
            signal = 'BUY'
        elif diff1 < 0 and diff2 > 0:
            signal = 'SELL'
        else:
            signal = None

        # Step 3: update state AFTER signal
        self.prev_prev = self.prev
        self.prev = data

        return signal