from checker import checkk_logged_in
from flask import Flask, session

app = Flask(__name__)

app.secret_key = "Token_key_secret_2"

@app.route('/')
def hello() -> str:
    return "Hello My Main page"

@app.route('/page1')
@checkk_logged_in
def page1() -> str:
    return "Hello My page1"

@app.route('/page2')
@checkk_logged_in
def page2() -> str:
    return "Hello My page2"

@app.route('/page3')
@checkk_logged_in
def page3() -> str:
    return "Hello My page3"


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in'

@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out'
   


if __name__ == '__main__':
    app.run(debug=True)

