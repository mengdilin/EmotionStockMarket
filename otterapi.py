import json
import urllib2
import datetime #from datetime import date, timedelta
import time

#gets count for keyword on twitter from yesterday to today
def setup(keyword):
    todaytime=get_times()[1]
    yesterdaytime=get_times()[0]
    api="http://otter.topsy.com/searchdate.json?apikey=4263CB29307E40A28947A235B87A64C1&q=%23"+keyword+"&type=tweet&mintime="+yesterdaytime+"&maxtime="+todaytime
    request=urllib2.urlopen(api)
    result=json.loads(request.read())
    return result["response"]["total"]

#helper function for setup
def get_times():
    mintime=datetime.date.today() - datetime.timedelta(1)
    mintime=time.mktime(mintime.timetuple())
    mintime=str(mintime)
    maxtime=datetime.date.today() + datetime.timedelta(1)
    maxtime=time.mktime(maxtime.timetuple())
    maxtime=str(maxtime)
    return [mintime,maxtime]

#gets count for keyword on twitter from the last 5 minutes
def setup1(keyword):
    a=datetime.datetime.now()-datetime.timedelta(seconds=5*60)
    current=time.mktime(a.timetuple())
    api="http://otter.topsy.com/searchdate.json?apikey=4263CB29307E40A28947A235B87A64C1&q=%23"+keyword+"&type=tweet&mintime="+str(current)
    request=urllib2.urlopen(api)
    result=json.loads(request.read())
    return result["response"]["total"]

print setup1("happy")
print setup1("sad")
