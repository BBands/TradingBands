"""-----------------------------------------------
Name:        BollingerBands.py
Purpose:     Plot Bollinger bands and the bB indicators
Author:      John Bollinger, CFA, CMT
Created:     13/04/2023
Version:     1.0
Updated:     25/09/2023
Copyright:   (c) John Bollinger 2023
License:     MIT
-----------------------------------------------"""
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class TradingBands:
    """Calculate and plot a set of six trading bands."""
    def __init__(self):
        self.symbol = 'SPY'
        self.months = 12
        self.length = self.months * -21
        self.data = pd.DataFrame()
        self.x = 0

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

    def calcBBands(self, length, width):
        """Calculate Bollinger Bands."""
        self.data['middleBB'] = self.data['Close'].rolling(window=length).mean()
        self.data['upperBB'] = self.data['middleBB'] + width * self.data['Close'].rolling(window=length).std(ddof = 0)
        self.data['lowerBB'] = self.data['middleBB'] - width * self.data['Close'].rolling(window=length).std(ddof = 0)

    def calcBBIndicators(self, upper, middle, lower):
        """Calculate trading band indicators."""
        self.data['pctb'] = (self.data.Close - lower) / (upper - lower)
        self.data['BandWidth'] = (upper - lower) / middle

    def BollingerBars(self, a0, x, open_, high_, low_, close_, barwidth=1.0):
        """
        Plot Bollinger Bars.
        Parameters:
        ax : 'Axes'
            an Axes instance to plot to
        barwidth: float
            width of bars
        """
        for t in x:
            op = open_[t]
            hi = high_[t]
            lo = low_[t]
            cl = close_[t]
            if cl >= op:
                centerbar = Line2D(xdata=(t, t), ydata=(cl, op),
                    color='g', linewidth=barwidth, antialiased=True)
                topbar = Line2D(xdata=(t, t), ydata=(hi, cl),
                    color='b', linewidth=barwidth, antialiased=True)
                bottombar = Line2D(xdata=(t, t), ydata=(op, lo),
                    color='b', linewidth=barwidth, antialiased=True)
            else:
                centerbar = Line2D(xdata=(t, t), ydata=(op, cl),
                    color='r', linewidth=barwidth, antialiased=True)
                topbar = Line2D(xdata=(t, t), ydata=(hi, op),
                    color='b', linewidth=barwidth, antialiased=True)
                bottombar = Line2D(xdata=(t, t), ydata=(cl, lo),
                    color='b', linewidth=barwidth, antialiased=True)
            a0.add_line(centerbar)
            a0.add_line(topbar)
            a0.add_line(bottombar)
        a0.autoscale_view(True, True, True)

    def plotBBands(self):
        """Plot the trading bands."""
        self.length = self.months * -21
        finish = len(self.data)
        start = finish + self.length
        self.x = np.arange(start, finish)
        fig, (a0, a1, a2) = plt.subplots(nrows=3, ncols=1, \
            sharex=True, gridspec_kw={'height_ratios':[2, 1, 1]})
        a0.plot(self.x, self.data['upperBB'][self.length:], color = 'red', label='upperBB')
        a0.plot(self.x, self.data['middleBB'][self.length:], color = 'blue', label='middleBB')
        a0.plot(self.x, self.data['lowerBB'][self.length:], color = 'green', label='lowerBB')
        self.BollingerBars(a0, self.x, self.data['Open'], self.data['High'], self.data['Low'], self.data['Close'], barwidth=1.2)
        a0.text(0.01, 0.95, 'Courtesy www.BollingerBands.com', color='gray', fontsize=10, transform=a0.transAxes, ha='left', va='center')
        a0.set_ylabel('Bollinger Bands')
        a1.plot(self.x, self.data['pctb'][self.length:], color = 'blue')
        a1.axhline(y=0.0, linewidth=0.8, color='g')
        a1.axhline(y=0.5, linewidth=0.8, color='b')
        a1.axhline(y=1.0, linewidth=0.8, color='r')
        a1.set_ylabel('%b')
        a2.plot(self.x, self.data['BandWidth'][self.length:], color = 'blue')
        a2.set_ylim(0, None)
        a2.set_ylabel('BandWidth')
        a0.grid()
        a1.grid()
        a2.grid()
        fig.suptitle(self.symbol)
        fig.set_size_inches(12, 8)
        plt.xticks(self.x[::21], \
            [date.strftime('%d-%b-%y') for date in self.data.index[self.length::21]], \
            rotation=30, ha='right')
        plt.subplots_adjust(bottom=0.15, hspace=0)
        plt.show()

if __name__ == '__main__':
    # instantiate our class
    a = TradingBands()
    # set the symbol to use
    a.symbol = '^gspc'
    # declare length of plots
    a.months = 12
    # get Yahoo! data
    a.getYahooData()
    # calculate Bollinger Bands
    a.calcBBands(length = 20, width = 2)
    # calculate the indicators
    a.calcBBIndicators(a.data.upperBB, a.data.middleBB, a.data.lowerBB)
    # plot it
    a.plotBBands()

# That's all folks!
