from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    conn = sqlite3.connect('youtubenews.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM youtubenews")
    rows = cur.fetchall()
    rows = rows[:50] #최근50개만 추출
    return render_template("index.html", rows=rows)


@app.route('/report', methods=['GET', 'POST'])
def report():
    return render_template('index2.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('index3.html')


if __name__ == '__main__':
    app.run()
