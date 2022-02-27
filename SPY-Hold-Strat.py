# This is a simple tutorial algo that trades SPY.
# Strategy: Buy and hold SPY. Sell if it is up or down 10%. Wait 1 month before re-entering.
# Backtest results from 1/1/2020 to 1/1/2022:
# Return: 52.23%, PSR: 60.536%, Sharpe Ratio: 1.26, Average Win: 10.69%, Average Loss: -12.04%, Drawdown: 19%

# 2/26/22 Algorithmic Trading Using Python #4 tutorial
# https://www.youtube.com/watch?v=WQwyKfef80k

class AlgorithmicTradingUsingPython(QCAlgorithm):

    # Initialize Algorithm
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Backtest Date
        self.SetEndDate(2022, 1, 1)  # Set End Backtest Date
        self.SetCash(100000)  # Set Strategy Cash

        # Add SPY Equity Data
        # More examples: self.AddCrypto(), self.AddForex, self.AddFuture
        # Resolution spans from once per tick (millisecond) to monthly or custome timeframes
        spy = self.AddEquity("SPY", Resolution.Daily)

        # Default data adjustment mode is split and dividend adjusted data (easier to handle)
        # spy.setDataNormalizationMode(DataNormalizationMode.Raw)

        # Symbol Objects
        self.spy = spy.Symbol
        self.SetBenchmark("SPY")  # Make a benchmark for backtesting
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)  # Adjust for fees

        # More backtest data
        self.entryPrice = 0
        self.period = timedelta(31)
        self.nextEntryTime = self.Time

    # This funcion is called whenever a ticker bar ends in the data series.
    # (Basically every time it recieves data)
    # Should account for lookahead bias
    def OnData(self, data):

        # Check if data exists
        if not self.spy in data:
            return

            # price = data.Bars[self.py].Close
        price = data[self.spy].Close
        # price = self.Securities[self.spy].Close

        # Trade logic
        # First check if bot is invested
        if not self.Portfolio.Invested:

            # Buy and hold for a month
            if self.nextEntryTime <= self.Time:
                # self.setHoldings(self.spy, 1)  # Buy SPY with 1% of the portfolio
                self.MarketOrder(self.spy, int(self.Portfolio.Cash / price))

                # Log actions to help debug
                self.Log("BUY SPY @" + str(price))
                self.entryPrice = price
        # Exit position if the price is up or down 10% from the entry
        elif self.entryPrice * 1.1 < price or self.entryPrice * 0.9 > price:
            # self.Liguidate(self.spy)  # Liquidate specific ticker
            self.Liquidate()  # Liquidate all positions

            # Log actions
            self.Log("SELL SPY @" + str(price))

            # Set next entry time
            self.nextEntryTime = self.Time + self.period 