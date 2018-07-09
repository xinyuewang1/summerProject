import pickle
import numpy
import sys
import datetime

def main():
    with open('39A_40lr.pkl', 'rb') as f:
        model = pickle.load(f)
    routeDict = pickle.load(open('routeDict.pkl', 'rb'))
    for key, route in routeDict.items():
        if route == int(sys.argv[1]):
            source = key
        if route == int(sys.argv[2]):
            destination = key
    weather = sys.argv[3]
    now = sys.argv[4]
    inputList = [int(now), int(weather)]
    inputs=[0]*(destination-source)
    i = 0
    while source < destination:
        inputs[i] = inputList + timeValue() + routeFind(source) + monthWeek()
        source += 1
        i += 1
    return model.predict(inputs).sum()


def timeValue():
    timeList = [0]*7
    time = int(sys.argv[5])
    if time//3 == 0:
        pass
    elif time//3 == 8 or time == 00:
        timeList[6] = 1
    else:
        timeList[(time//4)-1] = 1
    return timeList

def monthWeek():
    monthList = [0]*5
    dayList = [0]*6
    month = sys.argv[6]
    day = sys.argv[7]
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

def routeFind(current):
    routeList = [0]*71
    routeList[current-1] = 1
    return routeList

print(main())
