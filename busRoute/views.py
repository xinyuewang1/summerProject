from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

def index(request):
    return render(request, 'busRoute/index.html', {})

def stops(request):
    return render(request, 'busRoute/stops.html', {})

def tourism(request):
    return render(request, 'busRoute/tourism.html',{})

def timeGenerator(request, chosen_time):

    ''''this is a very basic function to display a time chosen'''

    return JsonResponse("The departure time you chose is %s" % chosen_time, safe=False)

def returntimeGenerator(request, returnTime):

    '''This will basically return the return time chosen'''

    return JsonResponse("The return time you chose is %s" % returnTime, safe=False) 


def deptMonth(request, month):

    '''This will basically return the departure month chosen'''

    return JsonResponse("The departure date you chose is %s" % month, safe=False)

def retMonth(request, returnmonth):

    '''This will basically return the return month chosen'''

    return JsonResponse("The return date you chose is %s" % returnmonth, safe=False)  
