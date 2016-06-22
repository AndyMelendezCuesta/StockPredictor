#!/usr/bin/env python
#
#  Copyright (c) 2012, Jake Marsh  (http://jakemmarsh.com)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
from __future__ import division #import must be at the beginning of the file

import json, urllib2, time
from datetime import datetime
from datetime import date

from time import mktime
from scipy.stats import spearmanr #kendalltau, spearmanr, pearsonr
import numpy as np

from my_first_ystockquote import get_historical_prices
from my_first_neuralNetwork import NeuralNetwork

# #added:
# from sklearn.metrics import precision_recall_fscore_support 
# from sklearn.metrics import f1_score 

#when running it, in the terminal:
# Last login: Thu May 26 11:38:31 on ttys002
# Andreas-MacBook-Pro-2:~ andreamelendezcuesta$ cd Desktop
# Andreas-MacBook-Pro-2:Desktop andreamelendezcuesta$ cd StockPredictor
# Andreas-MacBook-Pro-2:StockPredictor andreamelendezcuesta$ python my_first_analyzer.py > my_first_output.txt
# and the output is poured in my_first_optimized.txt

# ================================================================

#normalize function
def normalizePrice(price, minimum, maximum):
    return ((2*price - (maximum + minimum)) / (maximum - minimum))

#denormalize function
def denormalizePrice(price, minimum, maximum):
    return (((price*(maximum-minimum))/2) + (maximum + minimum))/2


# ================================================================

def rollingWindow(seq, windowSize):
    it = iter(seq)
    #win is the iterative version of the given sequence (the 10 closing prices passed by historical prices)
    win = [it.next() for cnt in xrange(windowSize)] # First window
    yield win #array of arrays
    #print "win before loop: ", win 
    for e in it: # Subsequent windows
        win[:-1] = win[1:] #win (except the last item of the list) = win (except the first item of the list); win does not change
        win[-1] = e #the last value from the win list = e (element from the sequence-the 10 closing prices passed by historical prices)
        yield win #the first array win with the updated win arrays give a final win array of 6 arrays. This is why the length of rollingWindow(values, windowSize) is 6 
        #the new ordered sequence-the 10 closing prices passed by historical prices accomodated in a different way (some elements were excluded. Line 49 and 50)
    #print "win after loop: ", win


    #Basic info:
    # >>> a
    # [10, 11, 12, 13, 14]
    # >>> it = iter(a)
    # >>> print it
    # <listiterator object at 0x1021df850>
    # >>> win = [it.next() for cnt in xrange(5)]
    # >>> print win
    # [10, 11, 12, 13, 14]

      #  1 # explicitly write a generator function
      #  2 def double(L):
      #  3     for x in L:
      #  4         yield x*2
      #  5 
      #  6 # eggs will be a generator
      #  7 eggs = double([1, 2, 3, 4, 5])
      #  8 
      #  9 # the above is equivalent to ("generator comprehension"?)
      # 10 eggs = (x*2 for x in [1, 2, 3, 4, 5])
      # 11 
      # 12 # need to do this if you need a list
      # 13 eggs = list(double([1, 2, 3, 4, 5]))
      # 14 
      # 15 # the above is equivalent to (list comprehension)
      # 16 eggs = [x*2 for x in [1, 2, 3, 4, 5]]


def getMovingAverage(values, windowSize):
    movingAverages = []
     
    #Recall: the length of rollingWindow(values, windowSize) is 6 because in rollingWindow(values, windowSize) we modify the win array 5 times and we store it together with the first win array. The first win array with the updated win arrays give a final win array of 6 arrays.
    for w in rollingWindow(values, windowSize): #we iterate over the new ordered sequence-the 10 closing prices passed by historical prices accomodated in a different way (some elements were excluded. Line 49 and 50)
        print "This is w: " + str(w)
        movingAverages.append(sum(w)/len(w))
    print "rollingWindow(values, windowSize): ", rollingWindow(values, windowSize)
    print "moving averages from getMovingAverage: " + str(movingAverages)
    return movingAverages #averages from the new ordered sequence-the 10 closing prices passed by historical prices accomodated in a different way (some elements were excluded. Line 49 and 50)
    #Because the light of rollingWindow(values, windowSize) is 6, the length of movingAverages is 6


def getMinimums(values, windowSize):
    minimums = []

    for w in rollingWindow(values, windowSize):
        minimums.append(min(w))
    print "minimums from getMinimums: " + str(minimums)       
    return minimums #minimum values from the new ordered sequence-the 10 closing prices passed by historical prices accomodated in a different way (some elements were excluded. Line 49 and 50)
    #Because the length of rollingWindow(values, windowSize) is 6, the length of minimums is also 6 

def getMaximums(values, windowSize):
    maximums = []

    for w in rollingWindow(values, windowSize):
        maximums.append(max(w))
    print "maximums from getMaximums: " + str(maximums)
    return maximums #maximum values from the new ordered sequence-the 10 closing prices passed by historical prices accomodated in a different way (some elements were excluded. Line 49 and 50)
    #Because the length of rollingWindow(values, windowSize) is 6, the length of maximums is also 6  

# ================================================================

def getTimeSeriesValues(values, window):
    movingAverages = getMovingAverage(values, window)
    minimums = getMinimums(values, window)
    print "getTimeSeriesValues, minimums: "
    print minimums  #minimum values from the new ordered sequence-the 10 closing prices passed by historical prices accomodated in a different way (some elements were excluded. Line 49 and 50)

    maximums = getMaximums(values, window)
    print "getTimeSeriesValues, maximums: "
    print maximums  #maximum values from the new ordered sequence-the 10 closing prices passed by historical prices accomodated in a different way (some elements were excluded. Line 49 and 50)
    returnData = []

    # build items of the form [[average, minimum, maximum], normalized price]
    for i in range(0, len(movingAverages)): #movingAverages are the averages from the new ordered sequence-the 10 closing prices passed by historical prices accomodated in a different way (some elements were excluded. Line 49 and 50)
        inputNode = [movingAverages[i], minimums[i], maximums[i]]
        #print "inputNode from getTimeSeriesValues: ", inputNode
        price = normalizePrice(values[len(movingAverages) - (i + 1)], minimums[i], maximums[i])
        outputNode = [price] #result from using the normalization function
        #print "outputNode from getTimeSeriesValues: ", outputNode
        tempItem = [inputNode, outputNode] 
        #print "tempItem from getTimeSeriesValues: ", tempItem
        returnData.append(tempItem)
    #print "returnData from getTimeSeriesValues (obtained by: returnData.append(tempItem)): ", returnData
    return returnData
    #Because the leght of length of movingAverages is 6 the length of returnData is also 6. Details in Line 108
    # [[[699.7640014000001, 692.359985, 711.119995], [1.1897684489507219]], 
    #  [[702.7020018000001, 692.359985, 712.900024], [0.8266771547999481]], 
    #  [[708.8660034000001, 695.700012, 723.179993], [-0.5829705267991298]], 
    #  [[712.7839965999999, 701.429993, 723.179993], [-1.5268948045976969]], 
    #  [[715.1599976, 711.119995, 723.179993], [-4.111113285425096]], 
    #  [[715.102002, 710.830017, 723.179993], [-3.0437278582565743]]]



# ================================================================
# Calling get_historical_prices (from ystockquote_prev)
def getHistoricalData(symbol, chosen_date):
    historicalData = get_historical_prices(symbol, chosen_date)
    arrayHData = []
    for element in historicalData[1:]: #we ignore the array with the labels
        arrayHData.append(float(element[4])) #the closing price of the stock on the shown date
    print "arrayHData from getHistoricalData: ", arrayHData
    return arrayHData

# arrayHData from getHistoricalData:  
# [710.830017, 713.309998, 715.289978, 723.179993, 712.900024, 711.119995, 701.429993, 695.700012, 692.359985, 698.210022]
  

# ================================================================

def getTrainingData(symbol, chosen_date):
    historicalData = getHistoricalData(symbol, chosen_date)
    print "historical data"
    print historicalData

    # reverse it so we're using the most recent data first, ensure we only have 9 data points
    historicalData.reverse()
    #lendata = len(historicalData)
    #del historicalData[lendata:]
    del historicalData[5:] #we stay with the first 5 values and the rest is deleted
    #print "historicalData.reverse(), del historicalData[lendata:]"
    print "historicalData.reverse(), del historicalData[5:]"
    print historicalData

    # get five 5-day moving averages, 5-day lows, and 5-day highs, associated with the closing price
    trainingData = getTimeSeriesValues(historicalData, 5)

    return trainingData

    #This is trainingData: 
    #[[[699.7640014000001, 692.359985, 711.119995], [-0.37632901048560846]]] 



def getPredictionData(symbol, chosen_date):
    historicalData = getHistoricalData(symbol, chosen_date)

    # reverse it so we're using the most recent data first, then ensure we only have 5 data points
    historicalData.reverse()
    #lenpdata = int(round(0.6*len(historicalData))) 
    #del historicalData[lenpdata:]
    del historicalData[10:]
    #print "historicalData.reverse(),  del historicalData[lenpdata:]"
    print "historicalData.reverse(),  del historicalData[10:]"
    print historicalData

    # get five 5-day moving averages, 5-day lows, and 5-day highs
    predictionData = getTimeSeriesValues(historicalData, 5)
    #The length of getTimeSeriesValues(historicalData, 5) is 6. Details in Line 155 and 156
    # [[[699.7640014000001, 692.359985, 711.119995], [1.1897684489507219]], 
    #  [[702.7020018000001, 692.359985, 712.900024], [0.8266771547999481]], 
    #  [[708.8660034000001, 695.700012, 723.179993], [-0.5829705267991298]], 
    #  [[712.7839965999999, 701.429993, 723.179993], [-1.5268948045976969]], 
    #  [[715.1599976, 711.119995, 723.179993], [-4.111113285425096]], 
    #  [[715.102002, 710.830017, 723.179993], [-3.0437278582565743]]]

    #gets the index 0 from the array with index 0 from getTimeSeriesValues(historicalData, 5):
    #[699.7640014000001, 692.359985, 711.119995]
    predictionData = predictionData[0][0]
    print "This is the Prediction Data (predictionData[0][0]): "
    print predictionData
    return predictionData

    # This is the Prediction Data (predictionData[0][0]): 
    # [699.7640014000001, 692.359985, 711.119995]



# ================================================================

def analyzeSymbol(symbol, chosen_date):
    import datetime
    from datetime import date
    from datetime import timedelta

    year = int(chosen_date[:4])
    month = int(chosen_date[5:7])
    day = int(chosen_date[8:])

    end_date = datetime.date(year, month, day)
    
    if end_date >= datetime.date.today():
        statement = "Choose any date before today: " + str(datetime.date.today())
        return statement

    startTime = time.time()
    
    trainingData = getTrainingData(symbol, chosen_date)
    print "This is the trainingData: ", trainingData
 
    #This is the trainingData:  
    #[[[531.9904153999998, 524.052386, 539.172466], [1.0000000000000075]]]

    network = NeuralNetwork(inputNodes = 3, hiddenNodes = 3, outputNodes = 1)
    
    print "after creating network (object of class neuralNetwork)"
    network.train(trainingData) 

    # get rolling data for most recent day
    predictionData = getPredictionData(symbol, chosen_date)
    #Prediction Data:  [531.9904153999998, 524.052386, 539.172466]

    print "We have reached here :) !: "

    # get prediction
    returnPrice = network.test(predictionData)
    #returnPrice:  0.99412062515

    # de-normalize and return predicted stock price
    predictedStockPrice = denormalizePrice(returnPrice, predictionData[1], predictionData[2])
    #predictedStockPrice = 535.3611854361063

    # create return object, including the amount of time used to predict
    returnData = {}
    returnData['price'] = predictedStockPrice
    returnData['time'] = time.time() - startTime
    print "returnData (price, time): ", returnData
    return returnData

    # returnData (price, time):  {'price': 535.3611854361063, 'time': 0.46462297439575195}

# ================================================================

def clean_given_data(expecting, predicted):
    #Cleaning data
    import datetime
    from datetime import date
    exp = []
    pred = []
    date_today = str(datetime.date.today())
    statement = 'Choose any date before today: {}'.format(date_today)
    for i in range(len(expecting)):
    #i = 0
    #while i < len(expecting):
        if expecting[i] == statement or predicted[i] == statement:
            expecting.pop[i]
            predicted.pop[i]
        elif type(expecting[i]) is not str and type(predicted[i]) is not str: #for expected an 'h' appears when there is no stock price that day
            exp.append(float(expecting[i][1]))
            pred.append(predicted[i].values()[0])
        i += 1
    return (exp, pred)

def mean_abs_percent_error(y_true, y_pred):
    #Mean Absolute Percent Error
    #formula
    #i = 0
    total = 0
    for i in range(len(y_true)):
    #while i < len(y_true):
        total += abs(y_true[i] - y_pred[i])/abs(y_true[i])
        i += 1

    val = total/len(y_true)
    mean_abs_percent_val = val * 100
    return mean_abs_percent_val

def mean_abs_deviation(y_true, y_pred):
    #Mean Absolute Deviation
    #formula
    #i = 0
    total = 0
    #while i < len(y_true):
    for i in range(len(y_true)):
        total += abs(y_true[i] - y_pred[i])
        i += 1
    dev = total/len(y_true)
    return dev

def spearman_correlation(y_true, y_pred):
    """
    Calculate Spearman's rank correlation coefficient between ``y_true`` and
    ``y_pred``.

    :param y_true: The true/actual/gold labels for the data.
    :type y_true: array-like of float
    :param y_pred: The predicted/observed labels for the data.
    :type y_pred: array-like of float

    :returns: Spearman's rank correlation coefficient if well-defined, else 0
    """
    ret_score = spearmanr(y_true, y_pred)[0]
    return ret_score if not np.isnan(ret_score) else 0.0

def cumulative_forecast_error(y_true, y_pred):
    #Cumulative Forecast Error
    #formula
    #i = 0
    total = 0
    #while i < len(y_true):
    for i in range(len(y_true)):
        total += y_true[i] - y_pred[i]
        i += 1
    return total 

#6 This is my metric, the loss (total negative error)
#len(y_true)
#List the negative_values and show len(negative_values)
#add the negative_values and that is our metric, how much we have lost
#List the positive_values and show the len(positive_values)
#add the positive_values and that is the complement of our metric, how much we have lost 
#Check the difference between what we have gained and lost and find if this stock predictor is good enough for you
def metric_six(y_true, y_pred):
    negative_vals = []
    positive_vals = []
    errors_list = []
    #i = 0
    m6 = 0
    complement_m6 = 0
    #while i < len(y_true):
    for i in range(len(y_true)):
        error = y_true[i] - y_pred[i]
        if error < 0:
            negative_vals.append(error) 
            m6 += error
        else: 
            positive_vals.append(error)
            complement_m6 += error
        errors_list.append(error)
        i += 1
    my_metric = [errors_list, negative_vals, positive_vals, m6, complement_m6]
    return my_metric

#Calling functions from ystockquote.py and new_analyzer.py
def given_data():
    #the output from the following commented out code is at the bottom of this file
    # expected = []
    # predictions = []
    # #expected
    # expected.append(get_historical_prices('GOOG', '2015-04-27')[1]) #weekday (Friday) #all one day after, or the day after the weekend :)
    # #predicted
    # predictions.append(analyzeSymbol('GOOG', '2015-04-24')) #weekday (Friday)
    
    #the output related to the following code is not at the bottom of this file but in output_optimized.txt
    #first_expect
    expected = []
    predictions = []
    #expected
    expected.append(get_historical_prices('GOOG', '2015-04-27')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-04-13')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-04-13')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-04-15')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-04-08')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-04-07')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-04-16')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-04-10')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-01-02')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-01-21')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-02-18')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-04-21')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-05-27')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-07-07')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-09-02')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-11-28')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-12-26')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-05-11')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-01-04')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-01-19')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-02-16')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-03-28')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-05-09')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-05-13')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-05-16')[1]) #done
   

    expected.append(get_historical_prices('GOOG', '2015-01-02')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-01-20')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-01-21')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-01-22')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-02-02')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-02-04')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-03-19')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-03-20')[1]) #done 
    # expected.append(get_historical_prices('GOOG', '2014-01-03')[1]) #done ###########
    # expected.append(get_historical_prices('GOOG', '2014-04-02')[1]) #done ###########
    # expected.append(get_historical_prices('GOOG', '2014-04-04')[1]) #done ###########
    expected.append(get_historical_prices('GOOG', '2014-05-02')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2014-06-03')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-06-23')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2014-06-24')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2014-07-02')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-01-05')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2016-01-12')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2016-01-13')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-01-04')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2016-01-19')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-01-19')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-01-21')[1]) #done 


    expected.append(get_historical_prices('GOOG', '2015-01-28')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-01-29')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-03-23')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-03-25')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-04-02')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-04-06')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-04-06')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-05-04')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-07-03')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2014-07-07')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2014-07-22')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2014-07-14')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-08-04')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-08-04')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-08-04')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-08-18')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-02-02')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2016-02-03')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2016-02-04')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2016-02-05')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2016-02-08')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-02-09')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-02-10')[1]) #done


    expected.append(get_historical_prices('GOOG', '2015-06-02')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-06-03')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-06-04')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-06-15')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-06-29')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-07-20')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-10-02')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2015-11-02')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-07-15')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2014-08-11')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-08-12')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-08-15')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-09-08')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-09-15')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2014-10-15')[1]) #done
    expected.append(get_historical_prices('GOOG', '2014-12-03')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-03-04')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2016-03-09')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2016-03-11')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2016-04-04')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2016-04-04')[1]) #done
    expected.append(get_historical_prices('GOOG', '2016-05-02')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2016-05-11')[1]) #done 
    expected.append(get_historical_prices('GOOG', '2016-05-13')[1]) #done 


    #predictions

    predictions.append(analyzeSymbol('GOOG', '2015-04-24')) #weekday (Friday)
    predictions.append(analyzeSymbol('GOOG', '2015-04-11')) #weekday (Saturday)
    predictions.append(analyzeSymbol('GOOG', '2015-04-12')) #weekday (Sunday)
    predictions.append(analyzeSymbol('GOOG', '2015-04-14')) #weekday (Tuesday) #works!
    predictions.append(analyzeSymbol('GOOG', '2015-04-07')) #weekday (Tuesday) ##Works!
    predictions.append(analyzeSymbol('GOOG', '2015-04-06')) #weekday (Monday) 
    predictions.append(analyzeSymbol('GOOG', '2015-04-15')) #weekday (Wednesday)
    predictions.append(analyzeSymbol('GOOG', '2015-04-09')) #weekday (Thursday)
    predictions.append(analyzeSymbol('GOOG', '2014-01-01')) #holiday, New Years Day #Wednesday
    predictions.append(analyzeSymbol('GOOG', '2014-01-20')) #holiday, Martin Luther King, Jr. Day #Monday
    predictions.append(analyzeSymbol('GOOG', '2014-02-17')) #holiday, Washington's Birthday #Monday
    predictions.append(analyzeSymbol('GOOG', '2014-04-18')) #holiday, Good Friday #Friday
    predictions.append(analyzeSymbol('GOOG', '2014-05-26')) #holiday, Memorial Day #Monday
    predictions.append(analyzeSymbol('GOOG', '2014-07-04')) #holiday, Independence Day #Friday
    predictions.append(analyzeSymbol('GOOG', '2014-09-01')) #holiday, Labor Day #Monday
    predictions.append(analyzeSymbol('GOOG', '2014-11-27')) #holiday, Thanksgiving Day #Thursday
    predictions.append(analyzeSymbol('GOOG', '2014-12-25')) #holiday, Christmas Day #Thursday
    predictions.append(analyzeSymbol('GOOG', '2016-05-10')) #weekday (Tuesday)
    predictions.append(analyzeSymbol('GOOG', '2016-01-01')) #holiday, New Years Day #Friday
    predictions.append(analyzeSymbol('GOOG', '2016-01-18')) #holiday, Martin Luther King, Jr. Day #Monday
    predictions.append(analyzeSymbol('GOOG', '2016-02-15')) #holiday, Washington's Birthday, #Monday 
    predictions.append(analyzeSymbol('GOOG', '2016-03-25')) #holiday, Good Friday, #Friday 
    predictions.append(analyzeSymbol('GOOG', '2016-05-06')) #weekday (Friday)
    predictions.append(analyzeSymbol('GOOG', '2016-05-12')) #weekday (Thursday)
    predictions.append(analyzeSymbol('GOOG', '2016-05-14')) #weekday (Saturday)

    predictions.append(analyzeSymbol('GOOG', '2015-01-01')) #holiday, New Years Day #Thursday
    predictions.append(analyzeSymbol('GOOG', '2015-01-19')) #holiday, Martin Luther King, Jr. Day #Monday
    predictions.append(analyzeSymbol('GOOG', '2015-01-20')) #Tuesday
    predictions.append(analyzeSymbol('GOOG', '2015-01-21')) #Wednesday
    predictions.append(analyzeSymbol('GOOG', '2015-02-01')) #Sunday
    predictions.append(analyzeSymbol('GOOG', '2015-02-03')) #Tuesday
    predictions.append(analyzeSymbol('GOOG', '2015-03-18')) #Wednesday
    predictions.append(analyzeSymbol('GOOG', '2015-03-19')) #Thursday
    # predictions.append(analyzeSymbol('GOOG', '2014-01-02')) #Thursday
    # predictions.append(analyzeSymbol('GOOG', '2014-04-01')) #Tuesday
    # predictions.append(analyzeSymbol('GOOG', '2014-04-03')) #Thursday
    predictions.append(analyzeSymbol('GOOG', '2014-05-01')) #Thursday
    predictions.append(analyzeSymbol('GOOG', '2014-06-02')) #Monday
    predictions.append(analyzeSymbol('GOOG', '2014-06-20')) #Friday
    predictions.append(analyzeSymbol('GOOG', '2014-06-23')) #Monday
    predictions.append(analyzeSymbol('GOOG', '2014-07-01')) #Wednesday
    predictions.append(analyzeSymbol('GOOG', '2016-01-04')) #Monday
    predictions.append(analyzeSymbol('GOOG', '2016-01-11')) #Monday
    predictions.append(analyzeSymbol('GOOG', '2016-01-12')) #Tuesday
    predictions.append(analyzeSymbol('GOOG', '2016-01-03')) #Sunday
    predictions.append(analyzeSymbol('GOOG', '2016-01-15')) #Friday
    predictions.append(analyzeSymbol('GOOG', '2016-01-17')) #Sunday
    predictions.append(analyzeSymbol('GOOG', '2016-01-20')) #Wednesday


    predictions.append(analyzeSymbol('GOOG', '2015-01-27')) #Tuesday
    predictions.append(analyzeSymbol('GOOG', '2015-01-28')) #Wednesday
    predictions.append(analyzeSymbol('GOOG', '2015-03-21')) #Saturday
    predictions.append(analyzeSymbol('GOOG', '2015-03-24')) #Tuesday
    predictions.append(analyzeSymbol('GOOG', '2015-04-01')) #Wednesday
    predictions.append(analyzeSymbol('GOOG', '2015-04-02')) #Thursday
    predictions.append(analyzeSymbol('GOOG', '2015-04-03')) #Holiday, Good Friday
    predictions.append(analyzeSymbol('GOOG', '2015-05-01')) #Friday
    predictions.append(analyzeSymbol('GOOG', '2014-07-02')) #Wednesday
    predictions.append(analyzeSymbol('GOOG', '2014-07-03')) #Thursday
    predictions.append(analyzeSymbol('GOOG', '2014-07-21')) #Monday
    predictions.append(analyzeSymbol('GOOG', '2014-07-12')) #Saturday
    predictions.append(analyzeSymbol('GOOG', '2014-08-01')) #Friday
    predictions.append(analyzeSymbol('GOOG', '2014-08-02')) #Saturday
    predictions.append(analyzeSymbol('GOOG', '2014-08-03')) #Sunday
    predictions.append(analyzeSymbol('GOOG', '2014-08-16')) #Saturday
    predictions.append(analyzeSymbol('GOOG', '2016-02-01')) #Monday
    predictions.append(analyzeSymbol('GOOG', '2016-02-02')) #Tuesday
    predictions.append(analyzeSymbol('GOOG', '2016-02-03')) #Wednesday
    predictions.append(analyzeSymbol('GOOG', '2016-02-04')) #Thursday
    predictions.append(analyzeSymbol('GOOG', '2016-02-05')) #Friday
    predictions.append(analyzeSymbol('GOOG', '2016-02-07')) #Sunday
    predictions.append(analyzeSymbol('GOOG', '2016-02-09')) #Tuesday


    predictions.append(analyzeSymbol('GOOG', '2015-06-01')) #Monday
    predictions.append(analyzeSymbol('GOOG', '2015-06-02')) #Tuesday
    predictions.append(analyzeSymbol('GOOG', '2015-06-03')) #Wednesday
    predictions.append(analyzeSymbol('GOOG', '2015-06-12')) #Friday
    predictions.append(analyzeSymbol('GOOG', '2015-06-26')) #Friday
    predictions.append(analyzeSymbol('GOOG', '2015-07-17')) #Friday
    predictions.append(analyzeSymbol('GOOG', '2015-10-01')) #Thursday
    predictions.append(analyzeSymbol('GOOG', '2015-11-01')) #Sunday
    predictions.append(analyzeSymbol('GOOG', '2014-07-14')) #Monday
    predictions.append(analyzeSymbol('GOOG', '2014-08-10')) #Sunday
    predictions.append(analyzeSymbol('GOOG', '2014-08-11')) #Monday
    predictions.append(analyzeSymbol('GOOG', '2014-08-14')) #Thursday
    predictions.append(analyzeSymbol('GOOG', '2014-09-05')) #Friday
    predictions.append(analyzeSymbol('GOOG', '2014-09-12')) #Friday
    predictions.append(analyzeSymbol('GOOG', '2014-10-14')) #Tuesday
    predictions.append(analyzeSymbol('GOOG', '2014-12-02')) #Tuesday
    predictions.append(analyzeSymbol('GOOG', '2016-03-03')) #Thursday
    predictions.append(analyzeSymbol('GOOG', '2016-03-08')) #Tuesday
    predictions.append(analyzeSymbol('GOOG', '2016-03-10')) #Thursday
    predictions.append(analyzeSymbol('GOOG', '2016-04-01')) #Friday
    predictions.append(analyzeSymbol('GOOG', '2016-04-02')) #Saturday
    predictions.append(analyzeSymbol('GOOG', '2016-05-01')) #Sunday
    predictions.append(analyzeSymbol('GOOG', '2016-05-10')) #Tuesday
    predictions.append(analyzeSymbol('GOOG', '2016-05-12')) #Thursday
    print "expected: ", expected
    print "predictions: ", predictions
    return (expected, predictions)




def main():
    #Call given_data
    expecting, predicted = given_data()

    expect, predict = clean_given_data(expecting, predicted)

    #Metrics:
    #1. Mean Absolute Error
    #2. Mean Absolute Percent Error
    #3. Mean Absolute Deviation
    #4. r2-score
    #5. Spearman Correlation
    #6. metric6
    #7. complement of metric6
    #8. Cumulative Forecast Error
    #9. Average gain per stock price prediction
    #10. Average loss per stock price prediction
    #11. Average total gain per stock price prediction
    #12. Maximum loss (minimum error)
    #13. Maximum gain (maximum error)
    #14. Total probability of loss (negative values)
    #15. Total probability of gain (positive_values)
    
    #Important Source of Information: https://www.kaggle.com/forums/f/15/kaggle-forum/t/6270/what-s-the-best-way-to-measure-accuracy-significance-of-a-stock-prediction

    #Mean Absolute Error
    from sklearn.metrics import mean_absolute_error
    y_true = expect
    y_pred = predict
    print "length of y_true (expect): ", len(y_true)
    print "length of y_pred (predict): ", len(y_pred)

    print "y_true (expect) list: ", y_true 
    print "y_pred (predict) list: ", y_pred
    
    #1. Mean Absolute Error 
    mean_abs_value = mean_absolute_error(y_true, y_pred)
    print "mean absolute error", mean_abs_value
    #mean absolute error 20.2985884596

    #2. Mean Absolute Percent Error
    mean_abs_perc_value = mean_abs_percent_error(y_true, y_pred)
    print "mean absolute percent error: ", mean_abs_perc_value

    #3. Mean Absolute Deviation
    mean_abs_dev = mean_abs_deviation(y_true, y_pred)
    print "mean absolute deviation: ", mean_abs_dev

    #4. R-Squared
    from sklearn.metrics import r2_score
    r2_score_val = r2_score(y_true, y_pred)
    print "r2 score: ", r2_score_val

    #5. Spearman Correlation
    corr = spearman_correlation(y_true, y_pred)
    print "Spearman correlation: ", corr

    #6 This is my metric, the loss (total negative error)
    #len(y_true)
    #List the negative_values and show len(negative_values)
    #add the negative_values and that is our metric, how much we have lost
    #List the positive_values and show the len(positive_values)
    #add the positive_values and that is the complement of our metric, how much we have lost 
    #Check the difference between what we have gained and lost and find if this stock predictor is good enough for you
    list_of_errors, negative_values, positive_values, metric6, complement_metric6 = metric_six(y_true, y_pred)

    print "negative error list: ", negative_values
    print "positive error list: ", positive_values
    num_neg = len(negative_values)
    num_pos = len(positive_values)
    num_neg_percent = num_neg / len(y_true) * 100 
    num_pos_percent = num_pos / len(y_true) * 100
    #test length
    test = num_neg + num_pos
    if test == len(y_true):
        print "length is right!"
        print "length of negative error list: ", num_neg
        print "percetage of negative errors: ", num_neg_percent
        print "length of positive error list: ", num_pos
        print "percentage of positive errors: ", num_pos_percent
    #6. metric6
    print "metric#6: ", metric6
    #7. complement of metric6
    print "complement of metric#6: ", complement_metric6
    #Check if this is good enough for you
    #8. Cumulative Forecast Error
    cum_forecast_err = cumulative_forecast_error(y_true, y_pred)
    print "cumulative forecast error: ", cum_forecast_err        
    your_gain = complement_metric6
    your_loss = metric6
    average_gain_per_stock_price = your_gain / len(y_true)
    average_loss_per_stock_price = your_loss / len(y_true)
    average_total_gain_per_stock_price = average_gain_per_stock_price + average_loss_per_stock_price
    print "Now it is time to check if this Stock Predictor for daily stock prices is good enough for you"
    print "You gained (using the given data): ", your_gain 
    print "You lost (using the given data): ", your_loss
    gain_loss_difference = your_gain + your_loss #equivalent to #5. Cumulative forecast error
    print "Your final gain or Cumulative forecast error: ", gain_loss_difference #equivalent to #5. Cumulative forecast error
    #9. Average gain per stock price prediction
    print "Average gain per stock price: ", average_gain_per_stock_price
    #10. Average loss per stock price prediction
    print "Average loss per stock price: ", average_loss_per_stock_price
    #11. Average total gain per stock price prediction
    print "Average total gain per stock price: ", average_total_gain_per_stock_price
    #12. Maximum loss (minimum error)
    maximum_loss = min(list_of_errors)
    print "maximum loss: ", maximum_loss
    #13. Maximum gain (maximum error)
    maximum_gain = max(list_of_errors)
    print "maximum gain: ", maximum_gain
    #14. Total probability of loss (negative values)
    print "total probability of loss (negative values):", num_neg_percent
    #15. Total probability of gain (positive_values)
    print "total probability of gain (positive_values): ", num_pos_percent



if __name__ == "__main__":
    main()



#original code: 
# if __name__ == "__main__":
#     print analyzeSymbol('GOOG', '2015-04-24') 


# #Output (last 33 lines of the output when predicting only the first item inside given_data()):
# returnData (price, time):  {'price': 535.3611854361063, 'time': 1.4522960186004639}
# length of y_true (expect):  1
# length of y_pred (predict):  1
# y_true (expect) list:  [563.390015]
# y_pred (predict) list:  [535.3611854361063]
# mean absolute error 28.0288295639
# mean absolute percent error:  4.97503129584
# mean absolute deviation:  28.0288295639
# r2 score:  0.0
# Spearman correlation:  0.0
# negative error list:  []
# positive error list:  [28.028829563893623]
# length is right!
# length of negative error list:  0
# percetage of negative errors:  0.0
# length of positive error list:  1
# percentage of positive errors:  100.0
# metric#6:  0
# complement of metric#6:  28.0288295639
# cumulative forecast error:  28.0288295639
# Now it is time to check if this Stock Predictor for daily stock prices is good enough for you
# You gained (using the given data):  28.0288295639
# You lost (using the given data):  0
# Your final gain or Cumulative forecast error:  28.0288295639
# Average gain per stock price:  28.0288295639
# Average loss per stock price:  0.0
# Average total gain per stock price:  28.0288295639
# maximum loss:  28.0288295639
# maximum gain:  28.0288295639
# total probability of loss (negative values): 0.0
# total probability of gain (positive_values):  100.0
# There are less than 3 negative errors in the error list!
# There are less than 3 positive errors in the error list!