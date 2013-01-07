from pymongo import Connection
Connection=Connection('mongo.stuycs.org')

# to auth
def auth():
    db = Connection.admin
    res=db.authenticate('ml7','ml7')
    # connect to database

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
    deducts n(#of stock)*c(price per stock) - strings
    OUTLINE DONE
    """
    db=Connection['EmotionStock']
    user=db.players
    emotion={"emotion":stock, "amount":c}
    if hasMoney(name,n,c):
        if hasStock(name,stock):
            updateStock(name,stock,n)
        else:
            stocks=getStocks(name)
            nstocks=stocks.insert(emotion)
            players.update({'name':str(name)},{"$push":{'stocks':nstocks} } )
        changeMoney(name,n,c)

def changeMoney(name,n,c):
    """
    deducts money from account
    name:used to identify player
    n:number of stocks bought
    c:price per stock
    """
    db=Connection['EmotionStock']
    user=db.players
    cost=int(float(n))*int(float(c))
    myMoney=

def hasMoney(name,n,c):
    """
    verifies that user isn't bankrupt
    DONE
    """
    db=Connection['EmotionStock']
    user=db.players
    player=players.find({'name':str(name)})
    myMoney=float(player["money"])
    cost=int(n)*int(c)
    total=myMoney-cost
    return total>=0
    

#def updateStock

def hasStock(name,stock):
    """
    returns boolean: True if has 'stock'; False if it doesn't
    DONE
    """
    db=Connection['EmotionStock']
    user=db.players
    stocks=getStocks(name)
    return stocks.find({'name':str(stock)}).count()

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
    return player['stocks']
