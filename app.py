from flask import Flask
from flask import session,render_template,url_for,redirect,request
import urllib2,json
import googleauth,utils,otterapi
from bson import BSON, json_util

app = Flask(__name__)
app.secret_key="secret key" # Since we'll be using sessions

@app.route("/")
def index():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    return render_template("index.html",d=session['user'])

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template('login.html')
    elif request.form['button']=='GOOGLE':
        username=request.form['username']
        utils.add_user(username)
        session["user"]=username
        return redirect(url_for("profile"))

@app.route('/updateStocks')
def updateStocks():
    date=utils.get_date()
    if (date == 0 or date < otterapi.get_times()[2]):
        utils.update_date(otterapi.get_times()[2])
        utils.update_market()
        return True
    else:
        return False

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for('login'))

@app.route('/getXcoords')
def getXcoords():
    updateStocks()
    return json.dumps(utils.get_market_x(),sort_keys=True,indent=4,default=json_util.default)

@app.route('/getYcoords')
def getYcoords():
    updateStocks()
    return json.dumps(utils.get_market_y(),sort_keys=True,indent=4,default=json_util.default)

@app.route('/getStocks/')
def getStocks():
    updateStocks()
    return json.dumps(utils.get_market(),sort_keys=True,indent=4,default=json_util.default)

@app.route('/stockNames')
def getStockNames():
    return json.dumps(utils.get_stocks_names(),sort_keys=True,indent=4,default=json_util.default)

@app.route('/profile',methods=["GET","POST"])

def profile():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    elif request.method=="GET":
        d=session['user']
        money=utils.get_money(d)
        stock=utils.get_stocks(d)
        soul=utils.get_soul(d)
        return render_template('profile.html',d=d,money=money,stock=stock,soul=soul)
    elif request.method=="POST":
        if request.form["button"]=="MARKET":
            return render_template("graph.html")
        elif request.form["button"]=="Logout":
            return redirect(url_for("logout"))
    return render_template("login.html")
        
        
#Oauth
'''
@app.route("/")
def index():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    return render_template("index.html",d=session['user'])

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.form['button']=='GOOGLE':
        #print "clicked"
        url=googleauth.build_redirect_url()
        return redirect(url)

@app.route("/googleoauth2callback")
def googleoauth2callback():
    # this code comes from the google login page
    code=request.args.get('code','')

    # if we didn't get a code, go back to login
    if code=='':
        return redirect(url_for('login'))

    # We have a code so we have to convert it to an access token
    access_token = googleauth.code_to_access_token(code)

    # and convert it to userinfo
    userinfo=googleauth.access_token_to_info(access_token)
    session['user']=userinfo
    return redirect(url_for('index'));
'''
if __name__=="__main__":
    app.debug=True
    app.run()
