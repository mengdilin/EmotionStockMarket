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
    return redirect(url_for(profile))

@app.route('/bank', methods=["GET","POST"])
def bank():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    elif request.method=="GET":
        d=session['user']
        soul=utils.get_soul(d)
        b=100-soul
        money=utils.get_money(d)
        return render_template('bank.html', d=d, soul=soul, b=b, money=money)
    elif request.method=="POST":
        button=request.form["button"]
        d=session["user"]
        if button=="Sell":
            amt_sell=int(request.form['selling'])
            value=utils.sell_soul(d,amt_sell)
            return redirect(url_for("bank"))
        elif button=="Buy":
            amt_buy=int(request.form['buying'])
            value=utils.buy_soul(d,amt_buy)
            return redirect(url_for("bank"))
    return redirect(url_for("profile"))

@app.route('/graph',methods=["GET","POST"])
def graph():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    prices=utils.get_market_y()
    sadp=prices["sad"][len(prices["sad"])-1]
    boredp=prices["bored"][len(prices["bored"])-1]
    lovep=prices["love"][len(prices["love"])-1]
    tiredp=prices["tired"][len(prices["tired"])-1]
    happyp=prices["happy"][len(prices["happy"])-1]
    sickp=prices["sick"][len(prices["sick"])-1]
    madp=prices["mad"][len(prices["mad"])-1]
    if request.method == "GET":
        return render_template("graph.html",bored="bored",boredp=boredp,lovep=lovep,tiredp=tiredp,happyp=happyp,sickp=sickp,madp=madp,sadp=sadp);
    if request.method == "POST":
        d=session['user']
        value=request.form["button"]
        value=value.split(" ")
        if (str(value[1])=="buy"):
            text=request.form[str(value[0])]
            if (text!=""):
                utils.buy_stock(d,str(value[0]),int(text))
        if (str(value[1])=="sell"):
            text=request.form[str(value[0])+" sold"]
            if (text!=""):
                utils.sell_stock(d,str(value[0]),int(text))
        return render_template("graph.html",bored="bored",boredp=boredp,lovep=lovep,tiredp=tiredp,happyp=happyp,sickp=sickp,madp=madp,sadp=sadp);

'''
        if (value[1]=="buy"):
            utils.buy_stock(d,value[0],text)
'''       

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
    updateStocks()
    app.run()
