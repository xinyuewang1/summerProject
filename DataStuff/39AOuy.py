import pickle
import numpy
import sys
import datetime

def main():
    return estimatedTime()

def estimatedTime():
    with open('39A_40lr.pkl', 'rb') as f:
        model = pickle.load(f)
    routeDict = pickle.load(open('routeDict.pkl', 'rb'))
    for key, route in routeDict.itteritems():
        if route == sys.argv[1]:
            source = key
        if route == sys.argv[2]:
            destination = key
    routeList = [0]*71
    weather = sys.argv[3]
    inputList = [source, destination, weather]
    inputs = inputList + timeValue() + routeList + monthWeek()
    return model(inputs)


def timeValue():
    timeList = [0]*8
    time = sys.argv[4]
    if time//4 == 0:
        timeList[7] = 1
    elif time//4 == 8:
        timeList[6] = 1
    else:
        timeList[(time//4)-1] = 1
    return timeList

def monthWeek():
    monthList = [0]*5
    dayList = [0]*6
    month = sys.argv[5].month
    day = sys.argv[5].day
    months = ['Feb', 'Mar', 'Apr', 'May', 'Jun']
    if month == 'Jan':
        pass
    else:
        monthList[months.index(month)]
    days = ['Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
    if day == 'Mon':
        pass
    else:
        dayList[days.index(day)]
    return monthList + dayList





