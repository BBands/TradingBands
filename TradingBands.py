"""-----------------------------------------------
Name:        TradingBands.py
Purpose:     Plot six types of trading bands
Author:      John Bollinger, CFA, CMT
Created:     13/04/2023
Version:     1.1 # added norgate data
Updated:     25/09/2023
Copyright:   (c) John Bollinger 2023
License:     MIT
-----------------------------------------------"""
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class TradingBands:
    """Calculate and plot a set of six trading bands."""
    def __init__(self):
        self.symbol = 'SPY'
        self.months = 12
        self.data = pd.DataFrame()
        self.x = 0
        self.length = 0

    def getNorgateData(self):
        """Get the requested daily data from Norgate plus enough for indictor run up."""
        import norgatedata as nd
        # end with today
        end = dt.datetime.today()
        # start n months ago
        # add an extra 6 months for indicator precalc
        start = end - dt.timedelta(days=self.months*31 + 182)
        # get data in a pandas dataframe
        self.data = nd.price_timeseries(
        self.symbol, start_date=start, end_date=end,
        timeseriesformat = 'pandas-dataframe',
        stock_price_adjustment_setting = nd.StockPriceAdjustmentType.NONE)

    def getYahooData(self):
        """Get the requested daily data from Yahoo! plus enough for indictor run up."""
        import yfinance as yf
        # end with today
        end = dt.datetime.today()
        # start n months ago
        # add an extra 6 months for indictor precalc
        start = end - dt.timedelta(days=self.months*31 + 182)
        # get data in a pandas dataframe
        self.data = yf.download(self.symbol, start, end)

    def calcLedouxBands(self):
        """Calculate Ledoux Bands."""
        self.data['upperLedoux'] = self.data['High']
        self.data['lowerLedoux'] = self.data['Low']

    def calcPctBands(self, length, width):
        """Calculate Percent Bands."""
        self.data['middlePct'] = self.data['Close'].rolling(window=length).mean()
        self.data['upperPct'] = self.data['middlePct'] * (1 + width)
        self.data['lowerPct'] = self.data['middlePct'] / (1 + width)

    def calcDoncian(self, length):
        """Calculate Donchian Bands."""
        self.data['upperDonch'] = self.data['Close'].rolling(window=length).max()
        self.data['lowerDonch'] = self.data['Close'].rolling(window=length).min()

    def calcKeltner(self, length, width):
        """Calculate Keltner Bands."""
        self.data['middleKelt'] = self.data['Close'].ewm(span=length).mean()
        self.data['ATR'] = pd.concat([self.data.High.sub(self.data.Low), self.data.High.sub(self.data.Close.shift()), self.data.Low.sub(self.data.Close.shift())], axis=1).max(1).ewm(span=20).mean()
        self.data['upperKelt'] = self.data['middleKelt'] + width * self.data['ATR']
        self.data['lowerKelt'] = self.data['middleKelt'] - width * self.data['ATR']

    def calcBBands(self, length, width):
        """Calculate Bollinger Bands."""
        self.data['middleBB'] = self.data['Close'].rolling(window=length).mean()
        self.data['upperBB'] = self.data['middleBB'] + width * self.data['Close'].rolling(window=length).std(ddof = 0)
        self.data['lowerBB'] = self.data['middleBB'] - width * self.data['Close'].rolling(window=length).std(ddof = 0)

    def calcBEnvelopes(self, length, width):
        """Calculate Bollinger Envelopes."""
        self.data['upperBE'] = self.data['High'].rolling(window=length).mean() + width * self.data['High'].rolling(window=length).std(ddof = 0)
        self.data['lowerBE'] = self.data['Low'].rolling(window=length).mean() - width * self.data['Low'].rolling(window=length).std(ddof = 0)
        self.data['middleBE'] = (self.data['upperBE'] + self.data['lowerBE'] ) / 2

    def calcBandIndicators(self, upper, middle, lower):
        """Calculate trading band indicators."""
        self.data['pctb'] = (self.data.Close - lower) / (upper - lower)
        self.data['BandWidth'] = (upper - lower) / middle

    def plotbands(self, case):
        """Plot the trading bands."""
        self.length = self.months * -21
        finish = len(self.data)
        start = finish + self.length
        self.x = np.arange(start, finish)
        for band in case:
            plt.figure(figsize=(8, 4.5))
            if band == 'Ledoux':
                plt.plot(self.x, self.data['upperLedoux'][self.length:], color = 'red', label='Upper Ledoux Band')
                plt.plot(self.x, self.data['lowerLedoux'][self.length:], color = 'blue', label='Lower Ledoux Band')
            if band == 'Percent':
                plt.plot(self.x, self.data['upperPct'][self.length:], color = 'red', label='Upper Percent Band')
                plt.plot(self.x, self.data['middlePct'][self.length:], color = 'blue', label='Middle Band')
                plt.plot(self.x, self.data['lowerPct'][self.length:], color = 'green', label='Lower Percent Band')
            elif band == 'Keltner':
                plt.plot(self.x, self.data['upperKelt'][self.length:], color = 'red', label='Upper Keltner Band')
                plt.plot(self.x, self.data['middleKelt'][self.length:], color = 'blue', label='Middle Keltner Band')
                plt.plot(self.x, self.data['lowerKelt'][self.length:], color = 'green', label='Lower Keltner Band')
            elif band == 'Donchian':
                plt.plot(self.x, self.data['upperDonch'][self.length:], color = 'green', label='Upper Donchian')
                plt.plot(self.x, self.data['lowerDonch'][self.length:], color = 'red', label='Lower Donchian')
            elif band == "Bollinger":
                plt.plot(self.x, self.data['upperBB'][self.length:], color = 'red', label='upperBB')
                plt.plot(self.x, self.data['middleBB'][self.length:], color = 'blue', label='middleBB')
                plt.plot(self.x, self.data['lowerBB'][self.length:], color = 'green', label='lowerBB')
            elif band == 'Envelopes':
                plt.plot(self.x, self.data['upperBE'][self.length:], color = 'red', label='Upper Bollinger Envelope')
                plt.plot(self.x, self.data['middleBE'][self.length:], color = 'blue', label='Middle Bollinger Envelope')
                plt.plot(self.x, self.data['lowerBE'][self.length:], color = 'green', label='Lower Bollinger Envelope')
            if band != 'Ledoux':
                plt.plot(self.x, self.data['Close'][self.length:], color = 'black', label=self.symbol)
            if band == 'Envelopes':
                plt.title('Bollinger Envelopes')
            else:
                plt.title(band + ' Bands')
            plt.ylabel('Courtesy Bollinger Capital Management', alpha=0.7)
            plt.legend()
            plt.grid()
            plt.xticks(self.x[::21], \
                [date.strftime('%d-%b-%y') for date in self.data.index[self.length::21]], \
                rotation=30, ha='right')
            plt.show()

if __name__ == '__main__':
    # instantiate our class
    a = TradingBands()
    # set the symbol to use
    a.symbol = 'SPY'
    # declare self.length of plots
    a.months = 12
    # must choose one or the other
    a.getYahooData()
    #a.getNorgateData()
    # calculate Ledoux bands
    a.calcLedouxBands()
    # calculate percent bands
    a.calcPctBands(length = 21, width = 0.045)
    # calculate Keltner bands
    a.calcKeltner(length = 20, width = 2)
    # calculate Donchian bands
    a.calcDoncian(length = 20)
    # calculate Bollinger Bands
    a.calcBBands(length = 20, width = 2)
    # calculate Bollinger Envelopes
    a.calcBEnvelopes(length = 20, width = 1.5)
    # calc trading band indcators
    a.calcBandIndicators(a.data.upperBB, a.data.middleBB, a.data.lowerBB)
    # plot it!
    a.plotbands(['Ledoux','Percent', 'Keltner', 'Donchian', 'Bollinger', 'Envelopes'])

# That's all folks!
