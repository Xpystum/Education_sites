from flask import Flask, session

app = Flask(__name__)

app.secret_key = "Token_key_secret"

@app.route('/setuser/<user>')
def setuser(user: str) -> str:
    session['user'] = user
    return 'User value set to: ' + session['user']

@app.route('/getuser')
def getuser() -> str:
    return 'User value in currently set to: ' + session['user']

if __name__ == '__main__':
    app.run(debug=False)