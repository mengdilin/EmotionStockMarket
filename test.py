from pymongo import Connection
Connection=Connection('mongo.stuycs.org')

# to auth
def auth():
    db = Connection.admin
    res=db.authenticate('ml7','ml7')
    # connect to database

auth()
db=Connection['test_g_final']
users=db.players
user.insert({"name":"me","money":"100","soul":"100","stocks":{}})
res=users.find()
for line in res:
    print line
