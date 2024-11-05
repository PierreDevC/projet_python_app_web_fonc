from flask import Flask,render_template, request

import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def home():
        return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
