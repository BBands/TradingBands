"""-----------------------------------------------
Name:        TradingBands.py
Purpose:     Plot six types of trading bands
Author:      John Bollinger, CFA, CMT
Created:     13/04/2023
Copyright:   (c) John Bollinger 2023
Licence:     MIT
-----------------------------------------------"""
import datetime as dt
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

class TradingBands:
    """Calcualte and plot a set of six trading bands."""
    def __init__(self):
        self.symbol = 'SPY'
        self.data = pd.DataFrame()

    def getdata(self, months):
        """Get the requested daily data from Yahoo! plus enough for indictor run up."""
        # end with today
        end = dt.datetime.today()
        # start n months ago
        # add an extra 6 months for indictor precalc
        start = end - dt.timedelta(days=months*31 + 182)
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

    def plotbands(self, case, months):
        """Plot the trading bands."""
        length = months * -21
        for band in case:
            if band == 'Ledoux':
                plt.plot(self.data['upperLedoux'][length:], color = 'red', label='Upper Ledoux Band')
                plt.plot(self.data['lowerLedoux'][length:], color = 'blue', label='Lower Ledoux Band')
            if band == 'Percent':
                plt.plot(self.data['upperPct'][length:], color = 'red', label='Upper Percent Band')
                plt.plot(self.data['middlePct'][length:], color = 'blue', label='Middle Band')
                plt.plot(self.data['lowerPct'][length:], color = 'green', label='Lower Percent Band')
            elif band == 'Keltner':
                plt.plot(self.data['upperKelt'][length:], color = 'red', label='Upper Keltner Band')
                plt.plot(self.data['middleKelt'][length:], color = 'blue', label='Middle Keltner Band')
                plt.plot(self.data['lowerKelt'][length:], color = 'green', label='Lower Keltner Band')
            elif band == 'Donchian':
                plt.plot(self.data['upperDonch'][length:], color = 'green', label='Upper Donchian')
                plt.plot(self.data['lowerDonch'][length:], color = 'red', label='Lower Donchian')
            elif band == "Bollinger":
                plt.plot(self.data['upperBB'][length:], color = 'red', label='upperBB')
                plt.plot(self.data['middleBB'][length:], color = 'blue', label='middleBB')
                plt.plot(self.data['lowerBB'][length:], color = 'green', label='lowerBB')
            elif band == 'Envelopes':
                plt.plot(self.data['upperBE'][length:], color = 'red', label='Upper Bollinger Envelope')
                plt.plot(self.data['middleBE'][length:], color = 'blue', label='Middle Bollinger Envelope')
                plt.plot(self.data['lowerBE'][length:], color = 'green', label='Lower Bollinger Envelope')
            if band != 'Ledoux':
                plt.plot(self.data['Close'][length:], color = 'black', label=self.symbol)
            if band == 'Envelopes':
                plt.title('Bollinger Envelopes')
            else:
                plt.title(band + ' Bands')
            plt.ylabel('Courtesy Bollinger Capital Management', alpha=0.7)
            plt.legend()
            plt.grid()
            plt.xticks(rotation=20, ha='right')
            plt.show()

if __name__ == '__main__':
    # declare length of chart
    months = 12
    # instantiate our class
    a = TradingBands()
    # set the symbol
    a.symbol = 'SPY'
    # get two years of data
    a.getdata(months)
    # calculate Ledoux bands
    a.calcLedouxBands()
    # calculate Keltner bands
    a.calcPctBands(length = 21, width = 0.045)
    # calculate Keltner bands
    a.calcKeltner(length = 20, width = 2)
    # calculate Bollinger Bands
    a.calcDoncian(length = 20)
    # plot the bands
    a.calcBBands(length = 20, width = 2)
    # calculate Bollinger Bands
    a.calcBEnvelopes(length = 20, width = 1.5)
    # calculate Donchian Bands
    a.plotbands(['Ledoux','Percent', 'Keltner', 'Donchian', 'Bollinger', 'Envelopes'], months)

# That's all folks!
