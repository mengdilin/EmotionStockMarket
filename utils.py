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
    else:
        return False

#returns a list
def get_players():
    db=Connection['EmotionStock']
    names=[]
    for line in players.find():
        names.append(line['name'])
    return names

#returns an int
def get_money(user):
    if authenticate(user):
        db=Connection['EmotionStock']
        name=players.find_one({"name":user})
        return name["money"]
    else:
        return False

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

def market_setup():
    db=Connection["EmotionStock"]
    name=["happy","love","sad","tired","bored","mad","sick"]
    for name in names:
        count=otterapi.setup(name)
        stock={"stock":name,"last count":count[1],"data":[{"time":"01/14","price":400}]}
        market.insert(stock)

#return: list of stocks for a specific user
def get_stocks(user):
    db=Connection["EmotionStock"]
    if(authenticate(user)):
        name=players.find_one({"name":user})
        stock=[]
        for item in name["stocks"]:
            stock.append(item)
        return stock

#get all the stocks' data 
def get_market():
    db=Connection["EmotionStock"]
    stocks=[]
    for item in market.find():
        stocks.append(item)
    return stocks

#get all stocks' name in the market
def get_stocks_names():
    db=Connection["EmotionStock"]
    stocks=get_market()
    names=[]
    for item in stocks:
        names.append(str(item["stock"]))
    return names

#get a specific stock's dictionary 
def get_stock(name):
    db=Connection["EmotionStock"]
    return market.find_one({"stock":name})

#get a specific stock's price
def get_stock_price(name):
    stock=market.find_one({"stock":name})
    return stock["data"][len(stock["data"])-1]["price"]

#soul:int
def sell_soul(name,soul):
    db=Connection["EmotionStock"]
    if get_soul(name)<=soul:
        return False
    else:
        user=players.find_one({"name":name})
        user["money"]=user["money"]+soul*100
        user["soul"]=user["soul"]-soul
        if in_bank(name):
            buser=bank.find_one({"name":name})
            buser["soul"]=buser["soul"]+soul
            bank.update({"name":name},buser)
        else:
            nbalance={"name":name,"soul":soul}
            bank.insert(nbalance)
        players.update({"name":name},user)
        return True

def buy_soul(name,soul):
    db=Connection["EmotionStock"]
    user=players.find_one({"name":name})
    if get_bank_soul(name)>=soul and user["money"]>=soul*100:
        user["money"]=user["money"]-(soul*100)
        user["soul"]=user["soul"]+soul
        buser=bank.find_one({"name":name})
        buser["soul"]=buser["soul"]-soul
        bank.update({"name":name},buser)
        if buser["soul"]==0:
            bank.remove(buser)
        players.update({"name":str(name)},user)
        return True
    else:
        return False

#returns an int 
def get_soul(name):
    db=Connection["EmotionStock"]
    user=players.find_one({"name":name})
    return user["soul"]

def get_bank_soul(name):
    db=Connection["EmotionStock"]
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
testing purpose only
'''
def delete_players():
    db=Connection["EmotionStock"]
    players.drop()

def delete_market():
    db=Connection["EmotionStock"]
    market.drop()


if __name__=="__main__":
    #market_setup()
    name="mengdi"
    stock="happy"
    count=1
    print get_market()
    #add_user(name)
    #buy_stock(name,stock,count)
    #sell_soul(name,10)
    #buy_soul(name,10)
    #print bank.find_one({"name":"mengdi"})
    #print players.find_one({"name":"mengdi"})
