import numpy as np

class Metrics:
    def __init__(self,profit_curve,equity_curve):
        self.profit_curve=profit_curve
        self.equity_curve=equity_curve
    def win_rate(self):
        pnl = self.profit_curve
        if not pnl:
            return 0
        wins = [p for p in pnl if p > 0]
        return len(wins) / len(pnl)

    def max_drawdown(self):
        equity = np.array(self.equity_curve)
        peak = np.maximum.accumulate(equity)
        drawdown = (equity - peak) / peak
        return drawdown.min()

    def sharpe_ratio(self):
        returns = np.diff(self.equity_curve) / self.equity_curve[:-1]
        if np.std(returns) == 0:
            return 0
        return (np.mean(returns) / np.std(returns)) * np.sqrt(252)