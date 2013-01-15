from pymongo import Connection
import otterapi

Connection=Connection('mongo.stuycs.org')

# to auth
db = Connection.admin
res=db.authenticate('ml7','ml7')
players=db.players
market=db.market

def get_players():
    db=Connection['EmotionStock']
    names=[]
    for line in players.find():
        names.append(line['name'])
    return names

#name:string
def add_user(name):
    db=Connection['EmotionStock']
    if not name in get_players():
        player={"name":str(name),"money":10000,"soul":100,'stocks':[]}
        players.insert(player)

'''
parameters:
        name:string
returns:
        boolean
'''
def authenticate(name):
    db=Connection["EmotionStock"]
    if not name in get_players():
        return False
    return True

def auth_stock(name):
    db=Connection["EmotionStock"]
    stock=players.find_one({"stock":name})
    if stock == None:
        return False
    return True
'''
parameters:
      name:string
      stock:string
      count:int
returns:
      boolean
'''
def buy_stock(name,stock,count):
    db=Connection["EmotionStock"]
    if (authenticate(name) and auth_stock(stock)):
        user=players.find_one({"name":name})
        stocks={"stock":stock,"shares":count}
        cost=get_stock_price(stock)*count
        if (user["money"]<cost):
            return False
        else:
            user["money"]=user["money"]-cost
        user["stocks"].append(stocks)
        players.update({"name":name},user)
        return True
    return False

'''
parameters:
      name:string
      stock:string
      count:int
returns:
      boolean
'''
def sell_stock(name,stock,count):
    db=Connection["EmotionStock"]
    if (authenticate(name) and auth_stock(stock)):
        stocks=get_stocks(name)
        for item in stocks:
            if item["stock"]==stock:
                item["shares"]=item["shares"]-count
                if item["shares"]==0:
                    stocks.remove(item)
        user=players.find_one({"name":name})
        user["stocks"]=stocks
        gain=get_stock_price(stock)*count
        user["money"]=user["money"]+gain
        players.update({"name":name},user)
        return True
    return False

'''
parameters:
      name:string
returns:
      list of dictionaries
'''
def get_stocks(user):
    db=Connection["EmotionStock"]
    if(authenticate(user)):
        name=players.find_one({"name":user})
        stock=[]
        for item in name["stocks"]:
            stock.append(item)
        return stock

def market_setup():
    db=Connection["EmotionStock"]
    names=["happy","confused","surprised","mad","scared","bored","confident","loved"]
    for name in names:
        count=otterapi.setup(name)
        stock={"stock":name,"last count":count[1],"data":[{"time":"01/14","price":400}]}
        market.insert(stock)
    
def get_market():
    stocks=[]
    for item in market.find():
        stocks.append(item)
    return stocks

def get_stocks_names():
    stocks=get_market()
    names=[]
    for item in stocks:
        names.append(str(item["stock"]))
    return names

def get_stock_price(name):
    stock=market.find_one({"stock":name})
    return stock["data"][len(stock["data"])-1]["price"]
    




'''
called daily by JS timer
might be a bug since I assumed data is pushed to the end of the list
'''
def update_price(name):
    db=Connection["EmotionStock"]
    stock=market.find_one({"stock":name})
    count=otterapi.setup(name)[1]
    time=otterapi.setup(name)[0]
    price=stock["data"][len(stock["data"])-1]["price"]*(1+((count-stock["last count"])/100))
    data=({"time":time,"price":price})
    stock["last count"]=count
    market.update({"stock":name},{"$push":{"data":data}})
    
'''
def add_stock(name,stock,n,c):
    """
    calls changeMoney
    adds stock type & # of stocks
    deducts n(#of stock)*c(price per stock) from 'money'
    OUTLINE DONE
    """
    db=Connection['EmotionStock']
    user=db.players
    emotion={"emotion":stock, "amount":c}
    if hasMoney(name,n,c):
        if hasStock(name,stock):
            updateStock(name,stock,n,True)
        else:
            stocks=getStocks(name)
            nstocks=stocks.insert(emotion)
            users.update({'name':str(name)},{"$push":{'stocks':nstocks} } )
        changeMoney(name,n,c,True)

def remove_stock(name,stock,n,c):
    """
    calls changeMoney
    removes n amount from stock 'stock'
    adds n*c to 'money'
    """
    db=Connection['EmotionStock']
    user=db.players
    if hasStock(name,stock):
        updateStock(name,stock,n,False)
        changeMoney(name,n,c,False)
        

def changeMoney(name,n,c,buy):
    """
    Changes the money in a player's account after buy/sell stock
    name:used to identify player
    n:number of stocks
    c:price per stock
    'buy' is a boolean: True if buying stock; False otherwise
    DONE
    """
    db=Connection['EmotionStock']
    user=db.players
    cost=int(float(n))*int(float(c))
    myMoney=getMoney(name)
    if buy:
        myMoney=myMoney-cost
    else:
        myMoney=myMoney+cost
    user.update({'name':str(name)},{"$push": {"money":myMoney}})

def updateStock(name,stock,n,buy):
    """
    User already has stocks of a given emotion
    Updates the amount
    name: player
    stock: name of stock
    n: amount of stock
    buy: boolean; True if buying; False if selling
    DONE
    """
    #db=Collection['EmotionStock']
    #user=db.players
    myStocks=getStocks(name)
    thisStock=myStock.find({'emotion':str(stock)})
    orgAmt=thisStock['amount']
    newAmt=""
    if buy:
        newAmt=str(int(n)+int(orgAmt))
    else:
        newAmt=str(int(n)-int(orgAmt))
    if newAmt="0":
        myStocks.remove({"emotion":str(stock)}) #removes emotion if no stocks
    else:
        myStocks.update({"emotion":str(stock)},{"$push":{"amount":newAmt}})
    

def hasMoney(name,n,c):
    """
    verifies that user isn't bankrupt
    DONE
    """
    db=Connection['EmotionStock']
    user=db.players
    player=user.find({'name':str(name)})
    myMoney=float(player["money"])
    cost=int(n)*int(c)
    total=myMoney-cost
    return total>=0
    
def hasStock(name,stock):
    """
    returns boolean: True if has 'stock'; False if it doesn't
    DONE
    """
    stocks=getStocks(name)
    return (stocks.find({'name':str(stock)}).count())>0

def getStocks(name):
    """
    returns dictionary of stocks for a given player
    DONE
    """
    db=Connection['EmotionStock']
    user=db.players
    player=user.find({'name':str(name)})
    return player['stocks']

def getMoney(name):
    """
    returns player's money
    DONE
    """
    db=Connection['EmotionStock']
    user=db.players
    player=user.find({'name':str(name)})
    return float(player["money"])

'''

'''
testing purpose only
'''
def delete_players():
    players.drop()

def delete_market():
    market.drop()

def get_stock(name):
    return market.find_one({"stock":name})

if __name__=="__main__":
    #market_setup()
    name="mengdi"
    stock="happy"
    count=1
    #add_user(name)
    buy_stock(name,stock,count)
    #print players.find_one({"name":"mengdi"})

    

