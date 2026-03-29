class Portfolio:
    def __init__(self,capital=100000):
        self.capital=capital
        self.position=0
        self.entry_price=0
        self.equity_curve=[]
        self.profit_curve=[]
    def update(self,signal,price):
        if signal=='BUY' and self.position==0:
            self.entry_price=price    
            self.position=self.capital/price
        #    print(f"Entered position of {self.position} units at price {self.entry_price}")
        elif signal=='SELL' and self.position>0:
            exit_price=price
            gross = self.position*(exit_price-self.entry_price)
            cost = (0.001*exit_price*self.position)+(0.001*self.entry_price*self.position)
            profit = gross-cost
            self.capital+=profit
            print("Entry price:",self.entry_price,"Exit price:",exit_price,"Profit:",profit,"Capital:",self.capital)
        #    print(f"Exited position of {self.position} units at price {exit_price} with profit {profit}")
            self.profit_curve.append(profit)
            self.position=0
    def mark_to_market(self,price):
        if self.position!=0:
            unrealized = self.position*(price-self.entry_price)
            self.equity_curve.append(self.capital+unrealized)
        else:
            self.equity_curve.append(self.capital)            
            