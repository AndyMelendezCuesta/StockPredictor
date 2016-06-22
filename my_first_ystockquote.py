#!/usr/bin/env python
#
#  Copyright (c) 2007-2008, Corey Goldberg (corey@goldb.org)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.

#Note: The code was adjusted to always extract the stock price of any given date between 1995-2016 and the stock prices of the two previous days. (the end_date is the chosen date)     
#from pandas.tseries.holiday import get_calendar, HolidayCalendarFactory, GoodFriday
import urllib

'''
This is the "ystockquote" module.
This module provides a Python API for retrieving stock data from Yahoo Finance.
This module contains the following functions:
get_all(symbol)
get_price(symbol)
get_change(symbol)
get_volume(symbol)
get_avg_daily_volume(symbol)
get_stock_exchange(symbol)
get_market_cap(symbol)
get_book_value(symbol)
get_ebitda(symbol)
get_dividend_per_share(symbol)
get_dividend_yield(symbol)
get_earnings_per_share(symbol)
get_52_week_high(symbol)
get_52_week_low(symbol)
get_50day_moving_avg(symbol)
get_200day_moving_avg(symbol)
get_price_earnings_ratio(symbol)
get_price_earnings_growth_ratio(symbol)
get_price_sales_ratio(symbol)
get_price_book_ratio(symbol)
get_short_ratio(symbol)
get_historical_prices(symbol, start_yyyymmdd, end_yyyymmdd)
sample usage:
>>> import ystockquote
>>> print ystockquote.get_price('GOOG')
529.46
'''

def __request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    return urllib.urlopen(url).read().strip().strip('"')


def get_all(symbol):
    """
    Get all available quote data for the given ticker symbol.
    
    Returns a dictionary.
    """
    values = __request(symbol, 'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')
    data = {}
    data['price'] = values[0]
    data['change'] = values[1]
    data['volume'] = values[2]
    data['avg_daily_volume'] = values[3]
    data['stock_exchange'] = values[4]
    data['market_cap'] = values[5]
    data['book_value'] = values[6]
    data['ebitda'] = values[7]
    data['dividend_per_share'] = values[8]
    data['dividend_yield'] = values[9]
    data['earnings_per_share'] = values[10]
    data['52_week_high'] = values[11]
    data['52_week_low'] = values[12]
    data['50day_moving_avg'] = values[13]
    data['200day_moving_avg'] = values[14]
    data['price_earnings_ratio'] = values[15]
    data['price_earnings_growth_ratio'] = values[16]
    data['price_sales_ratio'] = values[17]
    data['price_book_ratio'] = values[18]
    data['short_ratio'] = values[19]

    
    
def get_price(symbol): 
    return __request(symbol, 'l1')


def get_change(symbol):
    return __request(symbol, 'c1')
    
    
def get_volume(symbol): 
    return __request(symbol, 'v')


def get_avg_daily_volume(symbol): 
    return __request(symbol, 'a2')
    
    
def get_stock_exchange(symbol): 
    return __request(symbol, 'x')
    
    
def get_market_cap(symbol):
    return __request(symbol, 'j1')
   
   
def get_book_value(symbol):
    return __request(symbol, 'b4')


def get_ebitda(symbol): 
    return __request(symbol, 'j4')
    
    
def get_dividend_per_share(symbol):
    return __request(symbol, 'd')


def get_dividend_yield(symbol): 
    return __request(symbol, 'y')
    
    
def get_earnings_per_share(symbol): 
    return __request(symbol, 'e')


def get_52_week_high(symbol): 
    return __request(symbol, 'k')
    
    
def get_52_week_low(symbol): 
    return __request(symbol, 'j')


def get_50day_moving_avg(symbol): 
    return __request(symbol, 'm3')
    
    
def get_200day_moving_avg(symbol): 
    return __request(symbol, 'm4')
    
    
def get_price_earnings_ratio(symbol): 
    return __request(symbol, 'r')


def get_price_earnings_growth_ratio(symbol): 
    return __request(symbol, 'r5')


def get_price_sales_ratio(symbol): 
    return __request(symbol, 'p5')
    
    
def get_price_book_ratio(symbol): 
    return __request(symbol, 'p6')
       
       
def get_short_ratio(symbol): 
    return __request(symbol, 's7')
    


#Adjusted to receive two inputs: symbol and chosen_date instead of symbol, start_date, end_date
def get_historical_prices(symbol, chosen_date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYY-MM-DD'
    
    Returns a nested list.
    """
    import datetime
    from datetime import date
    from datetime import timedelta
    
    #Test
    # >>> chosen_date = '2016-05-10'
    # >>> year = int(chosen_date[:4])
    # >>> month = int(chosen_date[5:7])
    # >>> day = int(chosen_date[8:])
    # >>> end_date = datetime.date(year, month, day)
    # >>> start_date = str(end_date - datetime.timedelta(days=2))

    past_n_days = 10 #fixed because we only care about the stock price of the chosen day and the stock prices of the two previous days

    year = int(chosen_date[:4])
    month = int(chosen_date[5:7])
    day = int(chosen_date[8:])

    end_date = datetime.date(year, month, day)
    
    if end_date > datetime.date.today():
        statement = "Choose any date before today: " + str(datetime.date.today())
        d0 = end_date
        d1 = datetime.date.today()
        delta = d0 - d1
        past_n_days += delta.days
        # from datetime import date
        # d0 = date(2008, 8, 18)
        # d1 = date(2008, 9, 26)
        # delta = d0 - d1
        # print delta.days
    if end_date == datetime.date.today():
        past_n_days += 1
    

    #assert end_date < datetime.date.today(), "chosen date must be any previous day from today: %r" % end_date
    #assert num == 4, "len of set is not 4: %r" % num #example

    #List of dates:
    date_list = [end_date - datetime.timedelta(days=x) for x in range(0, 3)]

    # >>> date_list = [end_date - datetime.timedelta(days=x) for x in range(0, 3)]
    # >>> print date_list
    # [datetime.date(2016, 5, 10), datetime.date(2016, 5, 9), datetime.date(2016, 5, 8)]

    #start_date = str(end_date - datetime.timedelta(days=past_n_days)) #doesn't work when we previously put from datetime import datetime  
    start_date = str(end_date - timedelta(days=past_n_days)) #code is always functional
    end_date = chosen_date

    # #month, day and year
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(end_date[5:7]) - 1) + \
          'e=%s&' % str(int(end_date[8:10])) + \
          'f=%s&' % str(int(end_date[0:4])) + \
          'g=d&' + \
          'a=%s&' % str(int(start_date[5:7]) - 1) + \
          'b=%s&' % str(int(start_date[8:10])) + \
          'c=%s&' % str(int(start_date[0:4])) + \
          'ignore=.csv'
    print "url"
    print url
    days = urllib.urlopen(url).readlines()
    data = [day[:-2].split(',') for day in days]
    return data


if __name__ == "__main__":
    print get_historical_prices('GOOG', '2016-05-30')

#output
##if __name__ == "__main__":
##    print get_historical_prices('GOOG', '2016-05-30')
# Andreas-MacBook-Pro-2:StockPredictor andreamelendezcuesta$ python ystockquote_edited.py
# url
# http://ichart.yahoo.com/table.csv?s=GOOG&d=4&e=30&f=2016&g=d&a=4&b=16&c=2016&ignore=.csv
# [['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Clos'], 
#  ['2016-05-25', '720.76001', '727.51001', '719.705017', '725.27002', '1629200', '725.2700'], 
#  ['2016-05-24', '706.859985', '720.969971', '706.859985', '720.090027', '1920400', '720.09002'], 
#  ['2016-05-23', '706.530029', '711.478027', '704.179993', '704.23999', '1320900', '704.2399'], 
#  ['2016-05-20', '701.619995', '714.580017', '700.52002', '709.73999', '1816000', '709.7399'], 
#  ['2016-05-19', '702.359985', '706.00', '696.799988', '700.320007', '1656300', '700.32000'], 
#  ['2016-05-18', '703.669983', '711.599976', '700.630005', '706.630005', '1763400', '706.63000'], 
#  ['2016-05-17', '715.98999', '721.52002', '704.109985', '706.22998', '1999500', '706.2299'], 
#  ['2016-05-16', '709.130005', '718.47998', '705.650024', '716.48999', '1316200', '716.4899']]


## if __name__ == "__main__":
##     print get_historical_prices('GOOG', '2016-05-26')
# Andreas-MacBook-Pro-2:StockPredictor andreamelendezcuesta$ python ystockquote_edited.py
# url
# http://ichart.yahoo.com/table.csv?s=GOOG&d=4&e=26&f=2016&g=d&a=4&b=15&c=2016&ignore=.csv
# [['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Clos'], 
#  ['2016-05-25', '720.76001', '727.51001', '719.705017', '725.27002', '1629200', '725.2700'], 
#  ['2016-05-24', '706.859985', '720.969971', '706.859985', '720.090027', '1920400', '720.09002'], 
#  ['2016-05-23', '706.530029', '711.478027', '704.179993', '704.23999', '1320900', '704.2399'], 
#  ['2016-05-20', '701.619995', '714.580017', '700.52002', '709.73999', '1816000', '709.7399'], 
#  ['2016-05-19', '702.359985', '706.00', '696.799988', '700.320007', '1656300', '700.32000'], 
#  ['2016-05-18', '703.669983', '711.599976', '700.630005', '706.630005', '1763400', '706.63000'], 
#  ['2016-05-17', '715.98999', '721.52002', '704.109985', '706.22998', '1999500', '706.2299'], 
#  ['2016-05-16', '709.130005', '718.47998', '705.650024', '716.48999', '1316200', '716.4899']]


##if __name__ == "__main__":
##    print get_historical_prices('GOOG', '2016-05-10')
# Andreas-MacBook-Pro-2:StockPredictor andreamelendezcuesta$ python ystockquote_edited.py
# url
# http://ichart.yahoo.com/table.csv?s=GOOG&d=4&e=10&f=2016&g=d&a=3&b=30&c=2016&ignore=.csv
# [['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Clos'], 
#  ['2016-05-10', '716.75', '723.50', '715.719971', '723.179993', '1563100', '723.17999'], 
#  ['2016-05-09', '712.00', '718.710022', '710.00', '712.900024', '1508400', '712.90002'], 
#  ['2016-05-06', '698.380005', '711.859985', '698.106995', '711.119995', '1826100', '711.11999'], 
#  ['2016-05-05', '697.700012', '702.320007', '695.719971', '701.429993', '1677400', '701.42999'], 
#  ['2016-05-04', '690.48999', '699.75', '689.01001', '695.700012', '1688600', '695.70001'], 
#  ['2016-05-03', '696.869995', '697.840027', '692.00', '692.359985', '1531000', '692.35998'], 
#  ['2016-05-02', '697.630005', '700.640015', '691.00', '698.210022', '1644100', '698.21002']]    
    

#original function ########################################

# def get_historical_prices(symbol, start_date, end_date):
#     """
#     Get historical prices for the given ticker symbol.
#     Date format is 'YYYYMMDD'
    
#     Returns a nested list.
#     """

#     url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
#           'd=%s&' % str(int(end_date[4:6]) - 1) + \
#           'e=%s&' % str(int(end_date[6:8])) + \
#           'f=%s&' % str(int(end_date[0:4])) + \
#           'g=d&' + \
#           'a=%s&' % str(int(start_date[4:6]) - 1) + \
#           'b=%s&' % str(int(start_date[6:8])) + \
#           'c=%s&' % str(int(start_date[0:4])) + \
#           'ignore=.csv'
#     print "url"
#     print url

#     days = urllib.urlopen(url).readlines()
#     data = [day[:-2].split(',') for day in days]
#     #print data 
#     return data

# if __name__ == "__main__":
#     print get_historical_prices('GOOG', '20160321', '20160323')

# Andreas-MBP-2:StockPredictor andreamelendezcuesta$ python ystockquote.py
# url
# http://ichart.yahoo.com/table.csv?s=GOOG&d=2&e=23&f=2016&g=d&a=2&b=21&c=2016&ignore=.csv
# [['Date',         'Open',       'High',        'Low',       'Close',    'Volume', 'Adj Clos'], 
#  ['2016-03-23', '742.359985', '745.719971', '736.150024', '738.059998', '1421900', '738.05999'], 
#  ['2016-03-22', '737.460022', '745.00',     '737.460022', '740.75',     '1264400', '740.7'], 
#  ['2016-03-21', '736.50',     '742.50',     '733.515991', '742.090027', '1831800', '742.09002']]

#######Alternative function, argument: past_n_days ###################

# from datetime import datetime, timedelta

# def get_historical_prices(symbol, past_n_days):
#     """
#     Get historical prices for the given ticker symbol.
#     Date format is 'YYYY-MM-DD'
    
#     Returns a nested list.
#     """
#     end_date = str(datetime.now())[:10]
#     start_date= str(datetime.now() - timedelta(days=past_n_days))[:10]

#     # #month, day and year
#     url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
#           'd=%s&' % str(int(end_date[5:7]) - 1) + \
#           'e=%s&' % str(int(end_date[8:10])) + \
#           'f=%s&' % str(int(end_date[0:4])) + \
#           'g=d&' + \
#           'a=%s&' % str(int(start_date[5:7]) - 1) + \
#           'b=%s&' % str(int(start_date[8:10])) + \
#           'c=%s&' % str(int(start_date[0:4])) + \
#           'ignore=.csv'
#     print "url"
#     print url
#     days = urllib.urlopen(url).readlines()
#     data = [day[:-2].split(',') for day in days]
#     return data

# if __name__ == "__main__":
#    print get_historical_prices('GOOG', 2)

# Andreas-MacBook-Pro-2:StockPredictor andreamelendezcuesta$ python ystockquote_prev.py
# url
# http://ichart.yahoo.com/table.csv?s=GOOG&d=2&e=16&f=2016&g=d&a=2&b=14&c=2016&ignore=.csv
# [['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Clos'], 
#  ['2016-03-16', '726.369995', '737.469971', '724.51001', '736.090027', '1572300', '736.09002'], 
#  ['2016-03-15', '726.919983', '732.289978', '724.77002', '728.330017', '1720100', '728.33001'], 
#  ['2016-03-14', '726.809998', '735.50', '725.150024', '730.48999', '1716900', '730.4899']]