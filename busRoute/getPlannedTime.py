import urllib.request, json
from bisect import *
from datetime import datetime

def getStopTime(route,stop):
    '''Take route and stop number, return the json file with timetable info for this certain stop route combination.'''
    with urllib.request.urlopen("https://data.dublinked.ie/cgi-bin/rtpi/timetableinformation?operator=bac&type=week&stopid="+
                                str(stop) + "&routeid=" + str(route) + "&format=json") as url:
        return json.loads(url.read().decode())


def findNextTime(timeList,t):
    '''return the closest greater time than t in timeList. '''
    #times = np.array(pd.to_timedelta(timeList), dtype=np.datetime64)#'<M8[ns]')
    #print(times.dtype)
    #print(type(t),t)
    #print(type(timeList),timeList)
    #timeList = sorted(set(timeList))
    i = bisect_right(timeList,t)
    if i != len(timeList):
        #          index, value
        time = datetime.strptime(timeList[i], '%H:%M:%S')
        return [i, time]
    pass


#def nextBus(t, route, stop, weekday, dest):
def nextBus(t, route, stop, weekday):
    '''
    Take the time and find the closest bus on schedule.
    In returned list--
    0: index in the dict
    1: second from midnight
    2: startdayofweek
    3: enddayofweek
    4: destination as a identifier.
    '''
    data = getStopTime(route, stop)
    nextBus = []
    # t = datetime.strptime(t,'%H:%M')

    for result in data['results']:
        #if result["destination"] == dest:

        if result["startdayofweek"] == "Monday" and result["enddayofweek"] == "Sunday":
            nextTime = findNextTime(result["departures"], t)
            if nextTime:
                nextTime.extend([result["startdayofweek"], result["enddayofweek"], result["destination"]])
                nextBus.append(nextTime)

        if weekday <= 4 and (
                result["startdayofweek"] == "Monday" and result["enddayofweek"] == "Friday"):  # weekday
            nextTime = findNextTime(result["departures"], t)
            if nextTime:
                nextTime.extend([result["startdayofweek"], result["enddayofweek"], result["destination"]])
                nextBus.append(nextTime)

        elif weekday == 5 and (
                result["startdayofweek"] == "Saturday" and result["enddayofweek"] == "Saturday"):  # Sat
            nextTime = findNextTime(result["departures"], t)
            if nextTime:
                nextTime.extend([result["startdayofweek"], result["enddayofweek"], result["destination"]])
                nextBus.append(nextTime)

    t = datetime.strptime(t, '%H:%M')
    #print(nextBus)
    # print(type(nextBus[0][1]))
    # print(nextBus[0][1])
    if nextBus:
        nextBus = min(nextBus, key=lambda d: d[1] - t)
        nextBus[1] = int((nextBus[1] - datetime(1900, 1, 1, 0, 0)).total_seconds())
        return nextBus
    else:
        raise ValueError("nextBus is empty.")

#_____Test_________
#nextBus("15:19",769,3,)


#def bus(time, route, start, end, weekday, dest):
def bus(time, route, start, end, weekday):

    '''
    Provide which bus will come next for a certain time. for a certain condition.
    :param time: take time from user
    :param route: which bus route
    :param start: start stop
    :param end: end stop
    :param weekday: which weekday
    :return: two planned time seconds in a day for two stops
    '''
    startStop = nextBus(time, route, start, weekday)
    #print(startStop)
    data = getStopTime(route, end)
    for result in data["results"]:
        if result["destination"] == startStop[4] and result["startdayofweek"] == startStop[2] and \
                result["enddayofweek"] == startStop[3]:
        #if result["startdayofweek"] == startStop[2] and result["enddayofweek"] == startStop[3]:
            try:
                desPlannedTime = int((datetime.strptime(result["departures"][startStop[0]],"%H:%M:%S") -
                                  datetime(1900,1,1,0,0)).total_seconds())
            except IndexError:
                print("Start stop info:", startStop)
    return startStop[1], desPlannedTime

# -----------------TEST-----------
#bus("11:30",'145',7574,768,1)