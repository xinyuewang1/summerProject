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
        days = ['Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        if self.day == 'Mon':
            pass
        else:
            dayList[days.index(self.day)]
        return monthList + dayList

    def routeFind(self, current):
        routeList = [0]*71
        routeList[current-1] = 1
        return routeList