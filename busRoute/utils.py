import pickle
import numpy as np
import os
from django.conf import settings
import urllib.request, json, operator
from busRoute import getPlannedTime
from datetime import datetime
import time


# Original Code from https://stackoverflow.com/questions/20252669/get-files-from-directory-argument-sorting-by-size
# Slightly modified
def get_files_by_file_size(dirname, reverse=False):
    """ Return list of file paths in directory sorted by file size """

    # Get list of files
    filepaths = []
    for basename in os.listdir(dirname):
        filename = os.path.join(dirname, basename)
        #print(filename)
        #?static / pickles / stopLists / 9_7132_4392.pkl
        if os.path.isfile(filename):
            filepaths.append(basename)
    #print(filepaths)

    # Re-populate list with filename, size tuples
    for i in range(len(filepaths)):
        filepaths[i] = (filepaths[i], os.path.getsize(dirname+filepaths[i]))

    #print(filepaths)
    # Sort list by file size
    # If reverse=True sort from largest to smallest
    # If reverse=False sort from smallest to largest
    filepaths.sort(key=lambda filename: filename[1], reverse=reverse)

    # Re-populate list with just filenames
    for i in range(len(filepaths)):
        filepaths[i] = filepaths[i][0]

    return filepaths


def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# --------Make a sorted list by size-------
#save_obj(get_files_by_file_size('static/pickles/stopLists/', True),'sortedStopList')


def load_obj(name):

    #print("The file path is", os.path.dirname(os.path.abspath(__file__)))
    if name.endswith('.pkl'):
        with open(os.path.join(settings.STATIC_ROOT, name), 'rb') as f:
            return pickle.load(f)
    with open(os.path.join(settings.STATIC_ROOT, name + '.pkl'), 'rb') as f:
        return pickle.load(f)

#---------------------TEST-------------------
#l = load_obj('static/pickles/sortedStopList')
#print(l)

def getFirstAndLastStops1(route, stop1, stop2):
    '''
    Take route and two stops on it, return the first and last stop of this route as identifier.
    Using API.
    :param stop1: input stop 1
    :param stop2: input stop 2
    :return: first and last stop
    '''
    with urllib.request.urlopen(
            "https://data.dublinked.ie/cgi-bin/rtpi/routeinformation?routeid=" + str(
                route) + "&operator=bac&format=json") as url:
        data = json.loads(url.read().decode())
        for result in data['results']:
            for stop in result['stops']:
                if stop['stopid'] == stop1:
                    continue
                if stop['stopid'] == stop2:
                    return result['stops'][0]['stopid'], result['stops'][-1]['stopid']


def getFirstAndLastStops2(route, stop1, stop2):
    '''
    Using routeDict flavor
    :param route: bus line, e.g.:39A (Haven't consider case sensitive yet)
    :param stop1: stop1 on route
    :param stop2: stop2 on route
    :return: first and last stop on this route
    '''
    for d in os.listdir('static/pickles/stopDicts'):
        if d.startswith(route):
            stopD = load_obj('pickles/stopDicts/' + d)

            if stop1 in stopD and stop2 in stopD:
                return (min(stopD.items(), key=operator.itemgetter(1))[0],
                        max(stopD.items(), key=operator.itemgetter(1))[0])


# This function is working, but one problem is that it will return the first route that matches, but meanwhile, it could
# not be the longest or most frequently used one.
# print(getFirstAndLastStops2('39A',769,793))

def getFirstAndLastStops3(route, stop1, stop2):
    '''
    Use a list to get it, I think it would be easier.
    :param route: route number
    :param stop1: stop1
    :param stop2: stop2
    :return: first stop and last stop of the route, also the position of stop1 and stop2 on it.
    '''
    path = 'pickles/stopLists/'
    for l in load_obj('pickles/sortedIdList'):
        #print("l:", l)
        if l.split('_')[0] == route:
            stopList = load_obj(path + l)
            print("stopList:", stopList)
            if stop1 in stopList and stop2 in stopList:
                progrnumber1 = stopList.index(stop1) + 1
                progrnumber2 = stopList.index(stop2) + 1
                print("prog numbers", progrnumber1, progrnumber1)
                # index starts with 0, progrnumber starts with 1
                if progrnumber1 < progrnumber2:
                     return stopList[0], stopList[-1], progrnumber1, progrnumber2

                else:
                    raise Exception("Wrong input order: The bus run from "+str(progrnumber1)+" to "+str(progrnumber2))


class Ett39A:

    def __init__(self, route, source, dest, precipitation, temp, timeStr, weekday, dateStr):
        self.route = route
        self.source = source
        self.dest = dest
        self.precipitation = precipitation
        self.temp = temp
        self.timeStr = timeStr
        self.dt = datetime.strptime(timeStr, '%H:%M')
        self.timeInSec = int((self.dt - datetime(1900, 1, 1, 0, 0)).total_seconds())
        # self.month = month
        self.weekday = weekday
        self.date = datetime.strptime(dateStr, "%m/%d/%Y")

    def timeValue(self):
        timeList = [0] * 7
        mark = 0
        for i in range(14400, 90001, 10800):
            if i < self.timeInSec < (i + 10800):
                timeList[mark] = 1
                break
            else:
                mark += 1

        '''
        if self.time//3 == 0:
            pass
        elif self.time//3 == 8 or self.time == 00:
            timeList[6] = 1
        else:
            timeList[(self.time//4)-1] = 1
            '''
        return timeList

    def ucdTerm(self):
        if datetime(2018, 1, 22) < self.date < datetime(2018, 4, 27) or self.date > datetime(2018, 9, 10):
            return 1
        else:
            return 0

    def estimatedTime(self):
        modelDir = 'pickles/models/'
        scalerDir = 'pickles/scalers/'
        # print("The file path is", os.path.dirname(os.path.abspath(__file__)))
        identifier = getFirstAndLastStops3(self.route, self.source, self.dest)
        print("identifier:",identifier)

        if identifier:
            try:
                model = load_obj(
                    modelDir + str(self.route) + '_' + str(identifier[0]) + '_' + str(identifier[1]) + '_model')
                scaler = load_obj(
                    scalerDir + str(self.route) + '_' + str(identifier[0]) + '_' + str(identifier[1]) + '_scaler')
            except FileNotFoundError:
                print("Cannot find model for Route", self.route, "From", str(identifier[0]), "To", str(identifier[1]))
                return -1

            '''
            routeDict = load_obj(open(os.path.join(settings.STATIC_ROOT, 'pickles/routeDict.pkl'), 'rb'))
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
            '''
            # Get destination headsign and distance

            #headsign, dis1, dis2 = None, None, None
            dis1, dis2 = None, None

            filPath = os.path.join(settings.STATIC_ROOT, 'pickles/stopDicts')
            for d in os.listdir(filPath):
                if d.startswith(str(self.route) + '_' + str(identifier[0]) + '_' + str(identifier[1])):
                    # headsign = d.split('_')[-1][:-4]
                    d = d.rsplit('.', 1)[0]
                    data = load_obj('pickles/stopDicts/' + d)
                    dis1 = data[self.source]
                    dis2 = data[self.dest]
                    break
            # print(headsign)
            # get time list
            # periodList = self.timeValue()
            # print(periodList)

            #plannedTime = getPlannedTime.bus(self.timeStr, self.route, self.source, self.dest, self.weekday, headsign)
            plannedTime = getPlannedTime.bus(self.timeStr, self.route, self.source, self.dest, self.weekday)

            inputList1 = [identifier[2], plannedTime[0], self.precipitation, self.weekday, dis1]
            inputList1.extend(self.timeValue())
            inputList1.append(self.temp)
            if self.weekday <= 4:
                inputList1.extend([1, 0])
            elif self.weekday == 5:
                inputList1.extend([0, 1])
            else:
                inputList1.extend([0, 0])
            inputList1.append(self.ucdTerm())
            # print(inputList)
            inputList2 = inputList1.copy()
            inputList2[0] = identifier[3]
            inputList2[1] = plannedTime[1]
            inputList2[4] = dis2
            #print(inputList1, inputList2)
            inputArr = np.array([inputList1, inputList2])
            # print(inputArr)
            inputArr = scaler.transform(inputArr)
            pred = model.predict(inputArr)
            return pred[1] - pred[0]

        else:
            raise Exception("Fail to map " + str(self.source) + " and " + str(self.dest) + "on the same route.")

    # def monthWeek(self):
    #     monthList = [0] * 5
    #     dayList = [0] * 6
    #     months = ['Feb', 'Mar', 'Apr', 'May', 'Jun']
    #     if self.month == 'Jan':
    #         pass
    #     else:
    #         monthList[months.index(self.month)]
    #     days = ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    #     if self.day == 'Monday':
    #         pass
    #     else:
    #         dayList[days.index(self.day)]
    #     return monthList + dayList

    # def routeFind(self, current):
    #     routeList = [0] * 71
    #     routeList[current - 1] = 1
    #     return routeList


# -------------------------Test set---------------
#route, source, dest, precipitation, temp, timeStr, weekday, dateStr
#tic = time.time()
#ett = Ett39A('67', 1444, 3913, 0, 18, "16:45", 3, "7/26/2018")
#print(ett.estimatedTime())
#print("Time:",time.time()-tic)

# class Ann39A:

#     def __init__(self, source, dest, plannedTime, rain, day, distanceTravelled, temp, timeSec, month, date):
#         self.source = source
#         self.dest = dest
#         self.plannedTime = plannedTime
#         self.time = timeSec
#         self.rain = rain
#         self.temp = temp
#         self.distanceTravelled = distanceTravelled
#         self.day = day
#         self.month = month
#         self.date = date
#         routeDict = pickle.load(open('pickles/routeDict.pkl', 'rb'))
#         for key, route in routeDict.items():
#             if route == int(self.source):
#                 self.sourceK = key
#             if route == int(self.dest):
#                 self.destK = key
#         distanceDict = pickle.load(open('','rb'))
#         for key, distance in distanceDict.items():
#             if key == int(self.source):
#                 self.sourceDist = distance
#             if key == int(self.dest):
#                 self.destDist = distance

#     def checkDirection(self):
#         if self.sourceK <= self.destK:
#             return True
#         elif self.sourceK > self.destK:
#             return False

#     def peakTimes(self):
#         peakList = [0]*7
#         for i in range(0, 7):
#             if int(self.time) > 14400+(i*10800) && int(self.time) <= 25200+(i*10800):
#                 peakList[i] = 1
#         return peakList

#     def isWeekendOrTerm(self):
#         weekOrTermList = [0]*3
#         weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
#         if self.day in weekday:
#             weekOrTermList[0] = 1
#         else:
#             weekOrTermList[1] = 1
#         if self.date >= '2016-01-25' && self.date <= '2016-04-29' 
#             || self.date >= '2016-05-09' && self.date <= '2016-05-21'
#             || self.date >= '2017-01-23' && self.date <= '2016-04-28'
#             || self.date >= '2016-05-08' && self.date <= '2016-05-19':
#             weekOrTermList[3] = 1
#         return weekOrTermList


#     def estimatedTime(self):
#         if self.checkDirection() == True:
#             with open('ann.pkl', 'rb') as f:
#                 model = pickle.load(f)
#         else:
#             with open('ann.pkl', 'rb') as f:
#                 model = pickle.load(f)
#         if self.sourceK == 1:
#             modelIn = [self.destK, float(self.rain), int(self.day), self.distanceTravelled] + self.peakTimes() + [self.temp] + self.isWeekendOrTerm()
#             return model.predict(modelIn)
#         else:
#             modelInS = [self.sourceK, float(self.rain), int(self.day), self.distanceTravelled] + self.peakTimes() + [self.temp] + self.isWeekendOrTerm()
#             modelInD = [self.destK, float(self.rain), int(self.day), self.distanceTravelled] + self.peakTimes() + [self.temp] + self.isWeekendOrTerm()

#             return model.predict(modelInS) - model.predict(modelInD)
