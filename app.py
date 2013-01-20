from flask import Flask
from flask import session,render_template,url_for,redirect,request
import urllib2,json
import googleauth,utils
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
        return render_template("graph.html")

@app.route('/updateStocks')
def updateStocks():
    if (update_date == 0 or update_date < otterapi.get_times()[2]):
        names=utils.get_stocks_names()
        for name in names:
            utils.update_price(name)
        return True
    else:
        return False

@app.route('/getStocks')
def getStocks():
    return json.dumps(utils.get_market(),sort_keys=True,indent=4,default=json_util.default)

#Oauth
'''
@app.route("/")
def index():
    if not session.has_key('user'):
        return redirect(url_for('login'))
    return render_template("index.html",d=session['user'])

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for('login'))

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

