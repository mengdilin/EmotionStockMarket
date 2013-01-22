import urllib,json

baseurl='https://accounts.google.com/o/oauth2/auth?scope=%s&state=unique&redirect_uri=%s&response_type=code&client_id=%s'
scope=urllib.quote('https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email')

# These are all from the Google api console
client_id=urllib.quote('550850080377.apps.googleusercontent.com')
redirect_url=urllib.quote('http://127.0.0.1:6007/auth2callback')
client_secret="YRuHw-xFTIYUONiSDo7Cok-5"

#later replace 127.0.0.1:5000 in redirect_url
original_url= 'http://127.0.0.1:6007'

test_url='http://127.0.0.1:6007'

# This makes the url that we should rediret the user to if they
# want to login using google
def build_redirect_url():
    url = baseurl%(scope,redirect_url,client_id)
    return url


def code_to_access_token(code):
    params=urllib.urlencode({'code':code
                             ,'client_id':client_id
                             ,'client_secret':client_secret
                             ,'redirect_uri':"http://127.0.0.1:6007/auth2callback"
                             ,'grant_type':'authorization_code'})
    
    f=urllib.urlopen('https://accounts.google.com/o/oauth2/token' ,params)
    result=f.read()
    resultdict = json.loads(result)
    return resultdict['access_token']



def access_token_to_info(access_token):
    f=urllib.urlopen('https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s'%(access_token))
    result=f.read()
    resultdict=json.loads(result)
    return resultdict

