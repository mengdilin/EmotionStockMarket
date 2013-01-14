from pymongo import Connection
Connection=Connection('mongo.stuycs.org')

# to auth
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
