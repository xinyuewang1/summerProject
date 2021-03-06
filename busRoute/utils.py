import pickle
import numpy as np
import os
from busApp.settings import STATIC_ROOT
from busRoute import getPlannedTime
from datetime import datetime


def load_obj(name):
    '''
    load a pkl object from name. Can take care of situation with pkl ends or not.
    :param name: name of the file if in current directory, directory/name if not.
    :return: loaded pkl file
    '''
    try:
        path = os.path.join(STATIC_ROOT, name).replace('\\', '/')
        if name.endswith('.pkl'):
            with open(path, 'rb') as f:
                return pickle.load(f)
        with open(path + '.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("\""+name+"\" not found")
        # raise FileNotFoundError("\"%s\" not found" %(name))
        return -3

# def getFirstAndLastStops1(route, stop1, stop2):
#     '''
#     Take route and two stops on it, return the first and last stop of this route as identifier.
#     Using API.
#     :param stop1: input stop 1
#     :param stop2: input stop 2
#     :return: first and last stop
#     '''
#     with urllib.request.urlopen(
#             "https://data.dublinked.ie/cgi-bin/rtpi/routeinformation?routeid=" + str(
#                 route) + "&operator=bac&format=json") as url:
#         data = json.loads(url.read().decode())
#         for result in data['results']:
#             for stop in result['stops']:
#                 if stop['stopid'] == stop1:
#                     continue
#                 if stop['stopid'] == stop2:
#                     return result['stops'][0]['stopid'], result['stops'][-1]['stopid']
#
#
# def getFirstAndLastStops2(route, stop1, stop2):
#     '''
#     Using routeDict flavor
#     :param route: bus line, e.g.:39A (Haven't consider case sensitive yet)
#     :param stop1: stop1 on route
#     :param stop2: stop2 on route
#     :return: first and last stop on this route
#     '''
#     for d in os.listdir('static/pickles/stopDicts'):
#         if d.startswith(route):
#             stopD = load_obj('pickles/stopDicts/' + d)
#
#             if stop1 in stopD and stop2 in stopD:
#                 return (min(stopD.items(), key=operator.itemgetter(1))[0],
#                         max(stopD.items(), key=operator.itemgetter(1))[0])
#
#
# # This function is working, but one problem is that it will return the first route that matches, but meanwhile, it could
# # not be the longest or most frequently used one.
# # print(getFirstAndLastStops2('39A',769,793))

def getFirstAndLastStops3(route, stop1, stop2):
    '''
    Use a list to get it, I think it would be easier.
    :param route: route number
    :param stop1: stop1
    :param stop2: stop2
    :return: first stop and last stop of the route, also the position of stop1 and stop2 on it.
    '''
    route = route.upper()
    path = 'pickles/stopLists/'
    for l in load_obj('pickles/sortedIdList'):

        if l.split('_')[0] == route:
            stopList = load_obj(path + l)

            if stop1 in stopList and stop2 in stopList:
                progrnumber1 = stopList.index(stop1) + 1
                progrnumber2 = stopList.index(stop2) + 1

                # index starts with 0, progrnumber starts with 1
                if progrnumber1 < progrnumber2:
                    return stopList[0], stopList[-1], progrnumber1, progrnumber2

                else:
                    return stopList[0], stopList[-1], progrnumber2, progrnumber1


class Ett39A:
    '''
    This class will create an instance of model and return the prediction result.
    '''

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
        # print("identifier:",identifier)

        if identifier:
            try:
                model = load_obj(
                    modelDir + str(self.route) + '_' + str(identifier[0]) + '_' + str(identifier[1]) + '_model')
                scaler = load_obj(
                    scalerDir + str(self.route) + '_' + str(identifier[0]) + '_' + str(identifier[1]) + '_scaler')
            except FileNotFoundError:
                # print("Cannot find model for Route", self.route, "From", str(identifier[0]), "To", str(identifier[1]))
                return -2

            dis1, dis2 = None, None

            filPath = os.path.join(STATIC_ROOT, 'pickles/stopDicts')
            for d in os.listdir(filPath):
                if d.startswith(str(self.route) + '_' + str(identifier[0]) + '_' + str(identifier[1])):
                    d = d.rsplit('.', 1)[0]
                    data = load_obj('pickles/stopDicts/' + d)
                    dis1 = data[self.source]
                    dis2 = data[self.dest]
                    break
            if dis1 and dis2:
                plannedTime = getPlannedTime.bus(self.timeStr, self.route, self.source, self.dest, self.weekday)

                inputList1 = [identifier[2], plannedTime[0], self.precipitation, self.weekday, dis1]
                inputList1.extend(self.timeValue())  # timeValue return a list
                inputList1.append(self.temp)
                if self.weekday <= 4:
                    inputList1.extend([1, 0])
                elif self.weekday == 5:
                    inputList1.extend([0, 1])
                else:
                    inputList1.extend([0, 0])
                inputList1.append(self.ucdTerm())

                inputList2 = inputList1.copy()
                inputList2[0] = identifier[3]
                inputList2[1] = plannedTime[1]
                inputList2[4] = dis2

                inputArr = np.array([inputList1, inputList2])

                inputArr = scaler.transform(inputArr)
                pred = model.predict(inputArr)
                return pred[1] - pred[0], 0
            else:
                return "Fail to find distance of stops", -6  # fail to find distance.

        else:
            error = "Fail to map " + str(self.source) + " and " + str(self.dest) + " on the same route."

            return error, -1


# -------------------------Test set---------------
#route, source, dest, precipitation, temp, timeStr, weekday, dateStr
# tic = time.time()
# ett = Ett39A('67', 1444, 3913, 0, 18, "16:45", 3, "7/26/2018")
# print(ett.estimatedTime())
# print("Time:",time.time()-tic)