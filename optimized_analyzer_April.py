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

from optimized_ystockquote import get_historical_prices
from optimized_neuralNetwork import NeuralNetwork
# #added:
# from sklearn.metrics import precision_recall_fscore_support 
# from sklearn.metrics import f1_score 

#1st Change:
#Previous import statement: from my_first_ystockquote import get_historical_prices
#New import statement: from optimized_ystockquote import get_historical_prices

#when running it, in the terminal:
# Last login: Thu May 26 11:38:31 on ttys002
# Andreas-MacBook-Pro-2:~ andreamelendezcuesta$ cd Desktop
# Andreas-MacBook-Pro-2:Desktop andreamelendezcuesta$ cd StockPredictor
# Andreas-MacBook-Pro-2:StockPredictor andreamelendezcuesta$ python optimized_analyzer.py > optimized_output_1st_change.txt

#2nd Change:

#Previous import statement: from my_first_neuralNetwork import NeuralNetwork
#New import statement: from optimized_neuralNetwork import NeuralNetwork
#Details of 2nd Change : Lines 365, 368 from optimized_neuralNetwork.py

#when running it, in the terminal:
# Last login: Thu May 26 11:38:31 on ttys002
# Andreas-MacBook-Pro-2:~ andreamelendezcuesta$ cd Desktop
# Andreas-MacBook-Pro-2:Desktop andreamelendezcuesta$ cd StockPredictor
# Andreas-MacBook-Pro-2:StockPredictor andreamelendezcuesta$ python optimized_analyzer.py > optimized_output_2nd_change.txt

#3rd Change:
#Previous import statement: from my_first_neuralNetwork import NeuralNetwork
#New import statement: from optimized_neuralNetwork import NeuralNetwork
#Details of 3rd Change : Lines 366, 377, 368 from optimized_neuralNetwork.py

#when running it, in the terminal:
# Last login: Thu May 26 11:38:31 on ttys002
# Andreas-MacBook-Pro-2:~ andreamelendezcuesta$ cd Desktop
# Andreas-MacBook-Pro-2:Desktop andreamelendezcuesta$ cd StockPredictor
# Andreas-MacBook-Pro-2:StockPredictor andreamelendezcuesta$ python optimized_analyzer.py > optimized_output_3rd_change.txt

#4th Change
#Edited getTrainingData, Line 202
# Andreas-MacBook-Pro-2:StockPredictor andreamelendezcuesta$ python optimized_analyzer.py > optimized_output_4th_change.txt


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
    # #The following 3 lines seem to be not needed:
    # # reverse it so we're using the most recent data first, ensure we only have 9 data points
    # historicalData.reverse()
    #lendata = len(historicalData)
    #del historicalData[lendata:]
    del historicalData[5:] #we stay with the first 5 values and the rest is deleted
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

    expected.append(get_historical_prices('GOOG', '2015-04-18')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-04-19')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-04-20')[1]) #done
    expected.append(get_historical_prices('GOOG', '2015-04-21')[1]) #done

    #predictions

    predictions.append(analyzeSymbol('GOOG', '2015-04-15')) #weekday (Friday)
    predictions.append(analyzeSymbol('GOOG', '2015-04-18')) #weekday (Saturday)
    predictions.append(analyzeSymbol('GOOG', '2015-04-19')) #weekday (Sunday)
    predictions.append(analyzeSymbol('GOOG', '2015-04-20')) #weekday (Tuesday) #works!


    print "expected: ", expected
    print "predictions: ", predictions
    return (expected, predictions)

import datetime as DT
from matplotlib import pyplot as plt
from matplotlib.dates import date2num
from matplotlib.dates import YearLocator

dataTrue, dataPred = [], []
def main_plot(y_true, y_pred):
    dataTrue = [(DT.datetime.strptime('2015-04-18', "%Y-%m-%d"), y_true[0]), 
    (DT.datetime.strptime('2015-04-19', "%Y-%m-%d"), y_true[1]),
    (DT.datetime.strptime('2015-04-20', "%Y-%m-%d"), y_true[2]),
    (DT.datetime.strptime('2015-04-21', "%Y-%m-%d"), y_true[3])]

    ###########################################
    dataPred = [(DT.datetime.strptime('2015-04-15', "%Y-%m-%d"), y_pred[0]),
    (DT.datetime.strptime('2015-04-18', "%Y-%m-%d"), y_pred[1]),
    (DT.datetime.strptime('2015-04-19', "%Y-%m-%d"), y_pred[2]),
    (DT.datetime.strptime('2015-04-20', "%Y-%m-%d"), y_pred[3])] 
    
    x1 = [date2num(date) for (date, value) in dataTrue]
    y1 = [value for (date, value) in dataTrue]

    x2 = [date2num(date) for (date, value) in dataPred]
    y2 = [value for (date, value) in dataPred]
    
    fig = plt.figure()

    graph = fig.add_subplot(111)

    # Plot the data as blue and green markers
    graph.plot(x1,y1,'bs', x2,y2, 'g^')

    # Set the xtick locations to correspond to just the dates you entered.
    graph.set_xticks(x1)
    import matplotlib.dates as mdates
    graph.format_xdata = mdates.DateFormatter("%Y-%m-%d")
    # Set the xtick labels to correspond to just the dates you entered.
    graph.set_xticklabels(
            [date.strftime("%Y-%m-%d") for (date, value) in dataTrue]
            )
    fig.autofmt_xdate(bottom=0.2, rotation=90, ha='right')

    import matplotlib as mpl
    mpl.rcParams['legend.numpoints'] = 1

    plt.legend(['Real stock prices', 'Predictions'])

    plt.xlabel('Dates')
    plt.ylabel('Stock Prices')
    plt.savefig('main_plot_April.png')
    plt.show()

def residual_plot(list_of_errors):
    ###########################################
    residual = [(DT.datetime.strptime('2015-04-18', "%Y-%m-%d"), list_of_errors[0]),
    (DT.datetime.strptime('2015-04-19', "%Y-%m-%d"), list_of_errors[1]),
    (DT.datetime.strptime('2015-04-20', "%Y-%m-%d"), list_of_errors[2]),
    (DT.datetime.strptime('2015-04-21', "%Y-%m-%d"), list_of_errors[3])] 

    rx = [date2num(date) for (date, value) in residual]
    ry = [value for (date, value) in residual]

    fig = plt.figure()

    graph = fig.add_subplot(111)

    # Plot the data as a red line with round markers
    residual_points = graph.plot(rx,ry, 'g^')

    # Set the xtick locations to correspond to just the dates you entered.
    graph.set_xticks(rx)
    import matplotlib.dates as mdates
    graph.format_xdata = mdates.DateFormatter("%Y-%m-%d")
    # Set the xtick labels to correspond to just the dates you entered.
    graph.set_xticklabels(
            [date.strftime("%Y-%m-%d") for (date, value) in residual]
            )
    fig.autofmt_xdate(bottom=0.2, rotation=90, ha='right')

    plt.legend(['Residuals'])
    plt.xlabel('Dates')
    plt.ylabel('Residual from Prediction')
    plt.savefig('residual_plot_April.png')
    plt.show()
    


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

    #calling the main plot function
    print "Here's the main plot!"
    main_plot(y_true, y_pred)

    #calling residual plot function
    print "Here's the residual plot!"
    residual_plot(list_of_errors)


if __name__ == "__main__":
    main()


#Output
# length of y_true (expect):  4
# length of y_pred (predict):  4
# y_true (expect) list:  [528.662379, 528.662379, 525.602352, 537.512456]
# y_pred (predict) list:  [538.0139031923524, 537.9879112791684, 537.988062702718, 540.4561430610571]
# mean absolute error 8.50161355882
# mean absolute percent error:  1.60925465108
# mean absolute deviation:  8.50161355882
# r2 score:  -3.2428786626
# Spearman correlation:  0.632455532034
# negative error list:  [-9.351524192352372, -9.325532279168442, -12.385710702718029, -2.9436870610570622]
# positive error list:  []
# length is right!
# length of negative error list:  4
# percetage of negative errors:  100.0
# length of positive error list:  0
# percentage of positive errors:  0.0
# metric#6:  -34.0064542353
# complement of metric#6:  0
# cumulative forecast error:  -34.0064542353
# Now it is time to check if this Stock Predictor for daily stock prices is good enough for you
# You gained (using the given data):  0
# You lost (using the given data):  -34.0064542353
# Your final gain or Cumulative forecast error:  -34.0064542353
# Average gain per stock price:  0.0
# Average loss per stock price:  -8.50161355882
# Average total gain per stock price:  -8.50161355882
# maximum loss:  -12.3857107027
# maximum gain:  -2.94368706106
# total probability of loss (negative values): 100.0
# total probability of gain (positive_values):  0.0
# Here's the main plot!
# Here's the residual plot!