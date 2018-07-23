import pickle
import numpy
import os
from django.conf import settings


class Ett39A():

    def __init__(self, source, dest, weather, time, month, day):
        self.source = source
        self.dest = dest
        self.weather = int(weather)
        self.time = int(time)
        self.month = month
        self.day = day
    
    def estimatedTime(self):
        print("The file path is", os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(settings.STATIC_ROOT, 'pickles/39A_40lr.pkl'), 'rb') as f:
            model = pickle.load(f)
        routeDict = pickle.load(open(os.path.join(settings.STATIC_ROOT, 'pickles/routeDict.pkl'), 'rb'))
        for key, route in routeDict.items():
            if route == int(self.source):
                source = key
            if route == int(self.dest):
                destination = key
        now = (self.time)*60
        inputList = [int(now), int(self.weather)]
        inputs=[0]*(destination - source)
        i = 0
        while source < destination:
            inputs[i] = inputList + self.timeValue() + self.routeFind(source) + self.monthWeek()
            source += 1
            i += 1
        return model.predict(inputs).sum()


    def timeValue(self):
        timeList = [0]*7
        if self.time//3 == 0:
            pass
        elif self.time//3 == 8 or self.time == 00:
            timeList[6] = 1
        else:
            timeList[(self.time//4)-1] = 1
        return timeList

    def monthWeek(self):
        monthList = [0]*5
        dayList = [0]*6
        months = ['Feb', 'Mar', 'Apr', 'May', 'Jun']
        if self.month == 'Jan':
            pass
        else:
            monthList[months.index(self.month)]
        days = ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if self.day == 'Monday':
            pass
        else:
            dayList[days.index(self.day)]
        return monthList + dayList

    def routeFind(self, current):
        routeList = [0]*71
        routeList[current-1] = 1
        return routeList


class Ann39A:

    def __init__(self, source, dest, plannedTime, rain, day, distanceTravelled, temp, timeSec, month, date):
        self.source = source
        self.dest = dest
        self.plannedTime = plannedTime
        self.time = timeSec
        self.rain = rain
        self.temp = temp
        self.distanceTravelled = distanceTravelled
        self.day = day
        self.month = month
        self.date = date
        routeDict = pickle.load(open('pickles/routeDict.pkl', 'rb'))
        for key, route in routeDict.items():
            if route == int(self.source):
                self.sourceK = key
            if route == int(self.dest):
                self.destK = key
        distanceDict = pickle.load(open('','rb'))
        for key, distance in distanceDict.items():
            if key == int(self.source):
                self.sourceDist = distance
            if key == int(self.dest):
                self.destDist = distance
    
    def checkDirection(self):
        if self.sourceK <= self.destK:
            return True
        elif self.sourceK > self.destK:
            return False

    def peakTimes(self):
        peakList = [0]*7
        for i in range(0, 7):
            if int(self.time) > 14400+(i*10800) && int(self.time) <= 25200+(i*10800):
                peakList[i] = 1
        return peakList
    
    def isWeekendOrTerm(self):
        weekOrTermList = [0]*3
        weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        if self.day in weekday:
            weekOrTermList[0] = 1
        else:
            weekOrTermList[1] = 1
        if self.date >= '2016-01-25' && self.date <= '2016-04-29' 
            || self.date >= '2016-05-09' && self.date <= '2016-05-21'
            || self.date >= '2017-01-23' && self.date <= '2016-04-28'
            || self.date >= '2016-05-08' && self.date <= '2016-05-19':
            weekOrTermList[3] = 1
        return weekOrTermList
        

    def estimatedTime(self):
        if self.checkDirection() == True:
            with open('ann.pkl', 'rb') as f:
                model = pickle.load(f)
        else:
            with open('ann.pkl', 'rb') as f:
                model = pickle.load(f)
        if self.sourceK == 1:
            modelIn = [self.destK, float(self.rain), int(self.day), self.distanceTravelled] + self.peakTimes() + [self.temp] + self.isWeekendOrTerm()
            return model.predict(modelIn)
        else:
            modelInS = [self.sourceK, float(self.rain), int(self.day), self.distanceTravelled] + self.peakTimes() + [self.temp] + self.isWeekendOrTerm()
            modelInD = [self.destK, float(self.rain), int(self.day), self.distanceTravelled] + self.peakTimes() + [self.temp] + self.isWeekendOrTerm()
            return model.predict(modelInS) - model.predict(modelInD)
