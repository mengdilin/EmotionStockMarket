from pymongo import Connection
Connection=Connection('mongo.stuycs.org')

# to auth
def auth():
    db = Connection.admin
    res=db.authenticate('ml7','ml7')
    # connect to database

auth()
db=Connection['test_g_final']
user=db.players
#db.players.drop()
#user.insert({"name":"me","money":"100","soul":"100","stocks":{}})
res=user.find()
for line in res:
    print line
l=user.find({"name":"me"})
print l
for item in l:
    print item["money"] #<- this is what i need to do!!!
#FIX FIX FIX!!!
#find() only prints a cursor...
