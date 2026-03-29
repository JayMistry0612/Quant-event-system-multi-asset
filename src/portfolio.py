class Portfolio:
    def __init__(self, capital=100000, cost_pct=0.0005, allocation_pct=0.2):
        self.capital = capital
        self.cost_pct = cost_pct
        self.allocation_pct = allocation_pct

        self.positions = {}       
        self.entry_prices = {}    

        self.equity_curve = []
        self.profit_curve = []

    def update(self, signal, symbol, price):
        
        if signal == 'BUY':
            if symbol not in self.positions:

                allocation = self.capital * self.allocation_pct
                quantity = allocation / price

                self.positions[symbol] = quantity
                self.entry_prices[symbol] = price

                cost = self.cost_pct * price * quantity
                self.capital -= cost

                print(f"BUY {symbol} @ {price}")

        
        elif signal == 'SELL':
            if symbol in self.positions:

                quantity = self.positions[symbol]
                entry_price = self.entry_prices[symbol]

                gross = quantity * (price - entry_price)

                cost = (
                    self.cost_pct * entry_price * quantity +
                    self.cost_pct * price * quantity
                )

                profit = gross - cost
                self.capital += profit

                self.profit_curve.append(profit)

                print(f"SELL {symbol} @ {price} | PnL: {profit}")

                del self.positions[symbol]
                del self.entry_prices[symbol]
    def mark_to_market(self, batch):

        unrealized = 0

        for sym, qty in self.positions.items():
            entry_price = self.entry_prices[sym]

            if sym in batch:
                current_price = batch[sym]['Close']
            else:
                continue  

            unrealized += qty * (current_price - entry_price)

        total_equity = self.capital + unrealized
        self.equity_curve.append(total_equity)