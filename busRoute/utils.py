import pickle
import numpy


class Ett39A():

    def __init__(self, source, dest, weather, time, month, day):
        self.source = source
        self.dest = dest
        self.weather = int(weather)
        self.time = int(time)
        self.month = month
        self.day = day
        routeDict = pickle.load(open('pickles/routeDict.pkl', 'rb'))
        for key, route in routeDict.items():
            if route == int(self.source):
                self.sourceK = key
            if route == int(self.dest):
                self.destK = key
    
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

    def checkDirection(self):
        if self.sourceK <= self.destK:
            return True
        elif self.sourceK > self.destK:
            return False

    def forwardInputs(self):
        now = (self.time)*3600
        inputList = [int(now), int(self.weather)]
        inputs=[0]*(self.destK - self.sourceK)
        i = 0
        while self.sourceK < self.destK:
            inputs[i] = inputList + self.timeValue() + self.routeFind(self.sourceK) + self.monthWeek()
            self.sourceK += 1
            i += 1
        return inputs
    
    def backwardInputs(self):
        now = (self.time)*3600
        inputList = [int(now), int(self.weather)]
        inputs=[0]*(self.sourceK - self.destK)
        i = 0
        while self.destK < self.sourceK:
            inputs[i] = inputList + self.timeValue() + self.routeFind(self.destK) + self.monthWeek()
            self.destK += 1
            i += 1
        return inputs

    
    def estimatedTime(self):
        if self.checkDirection() == True:
            modelIn = self.forwardInputs()
            with open('pickles/39A_40lr.pkl', 'rb') as f:
                model = pickle.load(f)
        elif self.checkDirection() == False:
            modelIn = self.backwardInputs()
            with open('pickles/39A_40lr.pkl', 'rb') as f:
                model = pickle.load(f)
        return model.predict(modelIn).sum()

