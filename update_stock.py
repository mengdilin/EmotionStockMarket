import utils,otterapi,time,threading
def updateStocks():
    date=utils.get_date()
    print "here"
    if (date == 0 or date < otterapi.get_times()[2]):
        utils.update_date(otterapi.get_times()[2])
        utils.update_market()
    threading.Timer(3600,updateStocks).start()
if __name__=="__main__":
    updateStocks()
