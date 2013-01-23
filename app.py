from flask import Flask
from flask import session,render_template,url_for,redirect,request
import urllib2,json
import googleauth,utils,otterapi
from bson import BSON, json_util
import time,threading

app = Flask(__name__)
app.secret_key="secret key" # Since we'll be using sessions

@app.route("/")
def index():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    return redirect(url_for("about"))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template('login.html')
    elif request.method=="POST":
        if request.form['button']=='GOOGLE':
            url=googleauth.build_redirect_url()
            return redirect(url)
        elif request.form['button']=='Login':
            username=request.form['username']
            utils.add_user(username)
            session["user"]=username
            return redirect(url_for("about"))
 
@app.route("/auth2callback")
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
    session['user']=userinfo['email']
    utils.add_user(userinfo['email'])
    return redirect(url_for('about'));


def updateStocks():
    date=utils.get_date()
    #print "here"
    if (date == 0 or date < otterapi.create_times()[5]):
        print [date,otterapi.create_times()[5]]
        utils.update_date(otterapi.create_times()[5])
        utils.update_market()
    #threading.Timer(1,updateStocks).start()
    
    

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

@app.route('/about', methods=["GET","POST"])
def about():
    if request.method=="GET":
        return render_template('about.html')


@app.route('/profile',methods=["GET","POST"])
def profile():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    elif request.method=="GET":
        d=session['user']
        money=utils.get_money(d)
        stock=utils.get_stocks(d)[0]
        soul=utils.get_soul(d)
        gain=utils.get_stocks(d)[1]
        total=money+gain
        return render_template('profile.html',d=d,money=money,stock=stock,soul=soul,gain=gain,total=total)
    return redirect(url_for('profile'))

@app.route('/bank', methods=["GET","POST"])
def bank():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    d=session['user']
    soul=utils.get_soul(d)
    b=100-soul
    money=utils.get_money(d)
    if request.method=="GET":
        return render_template('bank.html', d=d, soul=soul, b=b, money=money)
    elif request.method=="POST":
        button=request.form["button"]
        if button=="Sell":
            try:
                amt_sell=int(request.form['selling'])
                if amt_sell>100 or amt_sell<0 or amt_sell>soul:
                    return render_template("bank1.html",d=d,soul=soul,b=b,money=money)
                value=utils.sell_soul(d,amt_sell)
                return redirect(url_for("bank"))
            except Exception:
                return render_template("bank1.html",d=d,soul=soul,b=b,money=money)
        elif button=="Buy":
            try:
                amt_buy=int(request.form['buying'])
                if amt_buy>100 or amt_buy<0 or amt_buy>b:
                    return render_template("bank1.html",d=d,soul=soul,b=b,money=money)
                value=utils.buy_soul(d,amt_buy)
                return redirect(url_for("bank"))
            except Exception:
                return render_template("bank1.html",d=d,soul=soul,b=b,money=money)
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
    boredi=utils.get_icon("bored")
    sadi=utils.get_icon("sad")
    lovei=utils.get_icon("love")
    tiredi=utils.get_icon("tired")
    happyi=utils.get_icon("happy")
    sicki=utils.get_icon("sick")
    madi=utils.get_icon("mad")
 
    if request.method == "GET":
        return render_template("graph.html",bored="bored",boredp=boredp,lovep=lovep,tiredp=tiredp,happyp=happyp,sickp=sickp,madp=madp,sadp=sadp,boredi=boredi[0],sadi=sadi[0],lovei=lovei[0],tiredi=tiredi[0],happyi=happyi[0],sicki=sicki[0],madi=madi[0],boredip=boredi[1],loveip=lovei[1],tiredip=tiredi[1],happyip=happyi[1],sickip=sicki[1],madip=madi[1],sadip=sadi[1]);
    if request.method == "POST":
        d=session['user']
        value=request.form["button"]
        value=value.split(" ")
        if (str(value[1])=="buy"):
            text=request.form[str(value[0])]
            if (text!=""):
                try:
                    text=int(text)
                    holder=utils.buy_stock(d,str(value[0]),int(text))
                except Exception:
                    holder=False

        if (str(value[1])=="sell"):
            text=request.form[str(value[0])+" sold"]
            if (text!=""):
                try:
                    text=int(text)
                    holder=utils.sell_stock(d,str(value[0]),int(text))
                except Exception:
                    holder=False
        if (text=="" or holder == False):
            return redirect(url_for("crash"))
        else:
            return redirect(url_for("transact"))
        return render_template("graph.html",bored="bored",boredp=boredp,lovep=lovep,tiredp=tiredp,happyp=happyp,sickp=sickp,madp=madp,sadp=sadp);

'''



'''

@app.route("/crash", methods=['GET','POST'])
def crash():
    if request.method == "GET":
        prices=utils.get_market_y()
        sadp=prices["sad"][len(prices["sad"])-1]
        boredp=prices["bored"][len(prices["bored"])-1]
        lovep=prices["love"][len(prices["love"])-1]
        tiredp=prices["tired"][len(prices["tired"])-1]
        happyp=prices["happy"][len(prices["happy"])-1]
        sickp=prices["sick"][len(prices["sick"])-1]
        madp=prices["mad"][len(prices["mad"])-1]
        boredi=utils.get_icon("bored")
        sadi=utils.get_icon("sad")
        lovei=utils.get_icon("love")
        tiredi=utils.get_icon("tired")
        happyi=utils.get_icon("happy")
        sicki=utils.get_icon("sick")
        madi=utils.get_icon("mad")
        return render_template("graph1.html",bored="bored",boredp=boredp,lovep=lovep,tiredp=tiredp,happyp=happyp,sickp=sickp,madp=madp,sadp=sadp,boredi=boredi[0],sadi=sadi[0],lovei=lovei[0],tiredi=tiredi[0],happyi=happyi[0],sicki=sicki[0],madi=madi[0],boredip=boredi[1],loveip=lovei[1],tiredip=tiredi[1],happyip=happyi[1],sickip=sicki[1],madip=madi[1],sadip=sadi[1]);

@app.route("/success",methods=["GET","POST"])
def transact(): 
    if request.method == "GET":
        prices=utils.get_market_y()
        sadp=prices["sad"][len(prices["sad"])-1]
        boredp=prices["bored"][len(prices["bored"])-1]
        lovep=prices["love"][len(prices["love"])-1]
        tiredp=prices["tired"][len(prices["tired"])-1]
        happyp=prices["happy"][len(prices["happy"])-1]
        sickp=prices["sick"][len(prices["sick"])-1]
        madp=prices["mad"][len(prices["mad"])-1]
        boredi=utils.get_icon("bored")
        sadi=utils.get_icon("sad")
        lovei=utils.get_icon("love")
        tiredi=utils.get_icon("tired")
        happyi=utils.get_icon("happy")
        sicki=utils.get_icon("sick")
        madi=utils.get_icon("mad")
        return render_template("graph2.html",bored="bored",boredp=boredp,lovep=lovep,tiredp=tiredp,happyp=happyp,sickp=sickp,madp=madp,sadp=sadp,boredi=boredi[0],sadi=sadi[0],lovei=lovei[0],tiredi=tiredi[0],happyi=happyi[0],sicki=sicki[0],madi=madi[0],boredip=boredi[1],loveip=lovei[1],tiredip=tiredi[1],happyip=happyi[1],sickip=sicki[1],madip=madi[1],sadip=sadi[1]);
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

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for('login'))


@app.route("/auth2callback")
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
    print userinfo['email']
    return redirect(url_for('index'));
'''
if __name__=="__main__":
    app.debug=True
    app.run(port=6007)
