from pymongo import Connection
import otterapi
Connection=Connection('mongo.stuycs.org')

db=Connection.admin
res=db.authenticate('ml7','ml7')
players=db.players
market=db.market
bank=db.bank

#name:string
def add_user(name):
    db=Connection['EmotionStock']
    if not name in get_players():
        player={"name":str(name),"money":10000,"soul":100,'stocks':[]}
        players.insert(player)

def get_players():
    db=Connection['EmotionStock']
    names=[]
    for line in players.find():
        names.append(line['name'])
    return names

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

def market_setup():
    db=Connection["EmotionStock"]
    name=["happy","love","sad","tired","bored","mad","sick"]
    for name in names:
        count=otterapi.setup(name)
        stock={"stock":name,"last count":count[1],"data":[{"time":"01/14","price":400}]}
        market.insert(stock)

def get_stocks(user):
    db=Connection["EmotionStock"]
    if(authenticate(user)):
        name=players.find_one({"name":user})
        stock=[]
        for item in name["stocks"]:
            stock.append(item)
        return stock

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

#added by GY 1.15.12; not tested

#soul:string
def sell_soul(name,soul):
    db=Connection["EmotionStock"]
    if get_soul(name)<=int(soul):
        return False
    else:
        user=players.find_one({"name":name})
        user["money"]=user["money"]+int(soul)*100
        user["soul"]=user["soul"]-int(soul)
        if in_bank(name):
            buser=bank.find_one({"name":name})
            buser["soul"]=buser["soul"]+int(soul)
            bank.update({"name":name},buser)
        else:
            nbalance={"name":name,"soul":int(soul)}
            bank.insert(nbalance)
        players.update({"name":name},user)
        return True
def buy_soul(name,soul):
    db=Connection["EmotionStock"]
    user=players.find_one({"name":name})
    if get_bank_soul(name)>=int(soul) and user["money"]>=int(soul)*100:
        user["money"]=user["money"]-(int(soul)*100)
        user["soul"]=user["soul"]+int(soul)
        buser=bank.find_one({"name":name})
        buser["soul"]=buser["soul"]-soul
        if buser["soul"]==0:
            bank.remove(buser)
        else:
            bank.update({"name":name},buser)
        return True
    else:
        return False
def get_soul(name):
    user=players.find_one({"name":name})
    return user["soul"]
def get_bank_soul(name):
    if in_bank(name):
        user=bank.find_one({"name":name})
        return user["soul"]
    else:
        return -1
def in_bank(name):
    db=Connection["EmotionStock"]
    names=[]
    for line in bank.find():
        names.append(line["name"])
    if not name in names:
        return False
    return True

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
def auth():
    db = Connection.admin
    res=db.authenticate('ml7','ml7')
    # connect to database


def setup():
    """
    creates dict of 'Emotions'
    """
    elist=["happy","love","sad","tired","bored","mad","sick"]
    db=Connection["EmotionStock"]
    emotions=db.emotions
    for item in elist:
        

def add_user(name):
    """
    adds players to the database
    DONE
    """
    db=Connection['EmotionStock']
    users=db.players
    if not name in getPlayers():
        player={"name":str(name),"money":"1000","soul":"100",'stocks':{}}
        users.insert(player)

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
    DONE
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
    for item in thisStock:
        amt=item["amount"]
    orgAmt=amt
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

def getPlayers():
    """
    returns a list of the player's names
    DONE
    """
    db=Connection['EmotionStock']
    user=db.players
    players=user.find()
    names=[]
    for line in players:
        names.append(line['name'])
    return names

def getStocks(name):
    """
    returns dictionary of stocks for a given player
    DONE
    """
    db=Connection['EmotionStock']
    user=db.players
    player=user.find({'name':str(name)})
    for item in player:
        result=item["stocks"]
    return result

def getMoney(name):
    """
    returns player's money
    DONE
    """
    db=Connection['EmotionStock']
    user=db.players
    player=user.find({'name':str(name)})
    for item in player:
        result=item["money"]
    return result

def getSoul(name):
    """
    returns value of 'soul' for a player
    """
    db=Connection["EmotionStock"]
    user=db.players
    player=user.find({"name":str(name)})
    for item in player:
        result=item["soul"]
    return result
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
