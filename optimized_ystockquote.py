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
    


########## Optimization of Input Data ###########
#Assumes that the end date is the chosen date and brings up the stock prices of the previous days
#Now I want to make sure that there are always a fixed set of stocks

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

    past_n_days = 20 #fixed because we only care about the stock price of the chosen day and the stock prices of the two previous days

    year = int(chosen_date[:4])
    month = int(chosen_date[5:7])
    day = int(chosen_date[8:])

    end_date = datetime.date(year, month, day)
    
    if end_date >= datetime.date.today():
        statement = "Choose any date before today: " + str(datetime.date.today())
        return statement

    #assert end_date < datetime.date.today(), "chosen date must be any previous day from today: %r" % end_date
    #assert num == 4, "len of set is not 4: %r" % num #example

    #start_date = str(end_date - datetime.timedelta(days=past_n_days)) #doesn't work when we previously put from datetime import datetime  
    start_date = str(end_date - timedelta(days=past_n_days)) #always works
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
    return data[0:11] #returns a set of 10 stock prices

#Example:
# if __name__ == "__main__":
#     print get_historical_prices('GOOG', '2014-04-03') #weekday (Friday)

#Output:
# url
# http://ichart.yahoo.com/table.csv?s=GOOG&d=3&e=3&f=2014&g=d&a=2&b=14&c=2014&ignore=.csv
# [['Date',          'Open',        'High',       'Low',       'Close',    'Volume', 'Adj Clos'],
#  ['2014-04-03', '569.852553', '587.282679', '564.132581', '569.742571', '5099100', '569.74257'], 
#  ['2014-04-02', '599.992707', '604.832763', '562.192568', '567.002574', '147100', '567.00257'], 
#  ['2014-04-01', '558.712504', '568.452595', '558.712504', '567.162558', '7900', '567.16255'], 
#  ['2014-03-31', '566.892592', '567.002574', '556.932537', '556.972503', '10800', '556.97250'], 
#  ['2014-03-28', '561.202549', '566.43259',  '558.672539', '559.992565', '41200', '559.99256'], 
#  ['2014-03-27', '568.00257',   '568.00257', '552.922516', '558.462551', '13100', '558.46255'], 
#  ['2014-03-26', '1162.012003', '1171.572011', '1131.501901', '1131.971918', '5179200', '565.42053'], 
#  ['2014-03-25', '1166.002007', '1169.842037', '1147.001947', '1158.722002', '4838400', '578.78221'], 
#  ['2014-03-24', '1184.192035', '1184.902085', '1145.952004', '1157.931941', '6096800', '578.38758'], 
#  ['2014-03-21', '1206.312028', '1209.632048', '1182.452014', '1183.041986', '6441000', '590.93006']]


################ original function ##################

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
#     print get_historical_prices('NZD', '20160321', '20160323')
#     print get_historical_prices('GOOG', '2016-01-02')
# Andreas-MBP-2:StockPredictor andreamelendezcuesta$ python ystockquote.py
# url
# http://ichart.yahoo.com/table.csv?s=NZD&d=2&e=23&f=2016&g=d&a=2&b=21&c=2016&ignore=.csv
# [['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Clos'], 
#  ['2016-03-23', '148.949997', '149.630005', '148.690002', '149.080002', '000', '149.08000'], 
#  ['2016-03-22', '148.210007', '148.479996', '147.619995', '148.059998', '000', '148.05999'], 
#  ['2016-03-21', '147.770004', '148.160004', '147.639999', '147.899994', '000', '147.89999']]

