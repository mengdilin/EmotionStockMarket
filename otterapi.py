import json
import urllib2
import datetime #from datetime import date, timedelta
import time

update_date=0
#gets time and count for keyword on twitter from yesterday to today
def setup(keyword):
    todaytime=get_times()[1]
    yesterdaytime=get_times()[0]
    api="http://otter.topsy.com/searchdate.json?apikey=4263CB29307E40A28947A235B87A64C1&q=%23"+keyword+"&type=tweet&mintime="+yesterdaytime+"&maxtime="+todaytime
    request=urllib2.urlopen(api)
    result=json.loads(request.read())
    yesterdaytime=real_time(float(yesterdaytime))

    return [yesterdaytime,result["response"]["total"]]

def pre_set(keyword, yesterdaytime, todaytime):
    api="http://otter.topsy.com/searchdate.json?apikey=4263CB29307E40A28947A235B87A64C1&q=%23"+keyword+"&type=tweet&mintime="+yesterdaytime+"&maxtime="+todaytime
    request=urllib2.urlopen(api)
    result=json.loads(request.read())
    yesterdaytime=real_time(float(yesterdaytime))
    return [yesterdaytime,result["response"]["total"]]

def get_date():
    mintime1=datetime.date.today() - datetime.timedelta(1)
    mintime1=float(time.mktime(mintime1.timetuple()))
    maxtime1=datetime.date.today()# - datetime.timedelta(1)
    maxtime1=float(time.mktime(maxtime1.timetuple()))
    return [mintime1,maxtime1]

def update(new_date):
    update_date=new_date

#helper function for setup
def get_times():
    mintime1=datetime.date.today() - datetime.timedelta(1)
    mintime=float(time.mktime(mintime1.timetuple()))
    maxtime1=datetime.date.today()
    maxtime=float(time.mktime(maxtime1.timetuple()))
    return [str(mintime),str(maxtime),mintime,maxtime]

#convert from unix time to real time
def real_time(atime):
    realtime=datetime.datetime.fromtimestamp(int(float(atime))).strftime('%m/%d')
    return realtime

#gets count for keyword on twitter from the last 5 minutes
def setup1(keyword):
    a=datetime.datetime.now()-datetime.timedelta(seconds=5*60)
    current=time.mktime(a.timetuple())
    api="http://otter.topsy.com/searchdate.json?apikey=4263CB29307E40A28947A235B87A64C1&q=%23"+keyword+"&type=tweet&mintime="+str(current)
    request=urllib2.urlopen(api)
    result=json.loads(request.read())
    return result["response"]["total"]


def create_times():
    t=[]
    for index in range(7):
        mintime1=datetime.date.today() - datetime.timedelta(index)
        mintime=float(time.mktime(mintime1.timetuple()))
        t.append(str(mintime))
    t.reverse()
    return t;

mintime=datetime.date.today()-datetime.timedelta(4)
mintime=float(time.mktime(mintime.timetuple()))
#print real_time(get_times()[2])
#rint pre_set("happy",str(get_date()[0]),str(get_date()[1]))
#print get_times()[0]
#print setup("love")
#love(200+);happy(90-100);bored(30-50);tired(10-20);sad(5-15);mad(0-10);sick(~20);excited(~20);

