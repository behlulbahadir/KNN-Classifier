import pandas as pd
import csv
import numpy as np
import math
import operator

df_train = pd.read_csv("train-post-operative.csv")
df_test = pd.read_csv("test-post-operative.csv")

def mod_data(df):
    df.replace('mid', 20, inplace=True)
    df.replace('low', 10, inplace=True)
    df.replace('excellent', 40, inplace=True)
    df.replace('stable', 20, inplace=True)
    df.replace('high', 30, inplace=True)
    df.replace('mod-stable', 10, inplace=True)
    df.replace('good', 30, inplace=True)
    df.replace('unstable', 0, inplace=True)
    df.replace('fair', 20, inplace=True)
    df.replace('poor', 10, inplace=True)

mod_data(df_train)
mod_data(df_test)

trainData = np.array(df_train)
testData = np.array(df_test)

def accuracy():
    predictions = []
    for i in range(len(testData)):
        output = {}
        for j in range(len(trainData)):
            distance = 0 
            distanceSqrt=0
            for x in range(8):
                distance += pow((trainData[j][x] - testData[i][x]), 2)
                distanceSqrt += math.sqrt(distance)
            output.update({j:distanceSqrt})
            sorted_output = sorted(output.items(), key=operator.itemgetter(1))
        index = sorted_output[i][0]
        predictions.append(trainData[index][8])

    count = 0
    for y in range(len(testData)):
        if(predictions[y] == testData[y][8]):
            count +=1

    acc = count/len(testData)*100
    print("%",acc)

def predictions():

    inputsName = [
        "L-CORE (patient's internal temperature in C) high (> 37), mid (>= 36 and <= 37), low (< 36) :",
        "L-SURF (patient's surface temperature in C) high (> 36.5), mid (>= 36.5 and <= 35), low (< 35) :",
        "L-O2 (oxygen saturation in %) excellent (>= 98), good (>= 90 and < 98), fair (>= 80 and < 90), poor (< 80) :",
        "L-BP (last measurement of blood pressure) high (> 130/90), mid (<= 130/90 and >= 90/70), low (< 90/70) :",
        "SURF-STBL (stability of patient's surface temperature) stable, mod-stable, unstable :",
        "CORE-STBL (stability of patient's core temperature) stable, mod-stable, unstable :",
        "BP-STBL (stability of patient's blood pressure) stable, mod-stable, unstable :",
        "COMFORT (patient's perceived comfort at discharge, measured as an integer between 0 and 20) :"
    ]

    data = []
    i = 0
    while i<8:
        data.append(input(inputsName[i]))
        i+=1

    with open('predictions.csv', mode='w') as predictions_file:
        fieldnames = ['L-CORE','L-SURF','L-O2','L-BP','SURF-STBL','CORE-STBL','BP-STBL','COMFORT']
        predictions_writer = csv.writer(predictions_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        predictions_writer.writerow(fieldnames)
        predictions_writer.writerow(data)
    
    df_predictions = pd.read_csv("predictions.csv")
    mod_data(df_predictions)
    predictionData = np.array(df_predictions)

    try:
        output = {}
        for j in range(len(trainData)):
            distance = 0 
            distanceSqrt=0
            for x in range(8):
                distance += pow((trainData[j][x] - predictionData[0][x]), 2)
                distanceSqrt += math.sqrt(distance)
            output.update({j:distanceSqrt})
            sorted_output = sorted(output.items(), key=operator.itemgetter(1))
        index = sorted_output[0][0]

        if (trainData[index][8] == 'A'):
            print("-------Hasta, hastane odasına gönderilecek-------")
        if(trainData[index][8] == 'S'):
            print("-------Hasta eve gönderilebilir-------")
        if(trainData[index][8] == 'I'):
            print("-------Hasta, Yoğun bakım ünitesine gönderilecek----")
    except TypeError:
        print("-------Hatalı giriş yaptınız--------")

accuracy()
predictions()