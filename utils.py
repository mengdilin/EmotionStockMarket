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
        players.insert(player)

def add_stock(name,stock,n,c):
    """
    calls changeMoney
    adds stock type and number of stock to 
    """
    db=Connection['EmotionStock']
    user=db.players
    emotion={"emotion":stock, "amount":c}
    if hasMoney(name):
        if hasStock(name,stock):
            updateStock(name,stock,n)
        else:
            me=players.find({'name':str(name)})
            players.update({'name':str(name)},{"$push":{'stocks':emotion} } )#need to fix
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

def hasMoney(name):
    """
    verifies that user isn't bankrupt
    """
    db=Connection['EmotionStock']
    user=db.players
    me=players.find({'name':str(name)})#wrong

#def updateStock
#def hasStock
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
