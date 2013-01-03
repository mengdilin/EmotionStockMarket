from pymongo import Connection
Connection=Connection('mongo.stuycs.org')

# to auth
def auth():
    db = Connection.admin
    res=db.authenticate('ml7','ml7')
    # connect to database

def add_user(name):
    db=Connection['EmotionStock']
    users=db.players
    if not name in getPlayers():
        player={"name":str(name),"money":"1000","soul":"100",'stocks':{}}
        players.insert(player)

def add_stock(name,stock,n,c):
    db=Connection['EmotionStock']
    user=db.players
    emotion={"emotion":stock, "amount":c}
    if hasMoney(name):
        changeMoney(name,n,c)
        if has_Stock(name,stock):
            update_stock(name,stock,n)
        else:
            players.update({'name':str(name)},{"$push":{'stocks':emotion} } )

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

def hasMoney(name):
    """
    verifies that user isn't bankrupt
    """
    db=Connection['EmotionStock']
    user=db.players
    me=players.find({'name':str(name)})

#def update_stock
#def has_stock
