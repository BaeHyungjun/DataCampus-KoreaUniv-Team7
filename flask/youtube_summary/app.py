from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('youtubenews.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT * FROM youtubenews")
rows = cur.fetchall()
rows = rows[:50]  # 최근50개만 추출


@app.route('/')
def home():
    return render_template("index.html", rows=rows)


@app.route('/report', methods=['GET', 'POST'])
def report():
    return render_template('index2.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('index3.html')


@app.route('/ytn', methods=['GET', 'POST'])
def ytn():
    return render_template("index_ytn.html", rows=rows)


@app.route('/kbs', methods=['GET', 'POST'])
def kbs():
    return render_template("index_kbs.html", rows=rows)


@app.route('/mbc', methods=['GET', 'POST'])
def mbc():
    return render_template("index_mbc.html", rows=rows)


@app.route('/sbs', methods=['GET', 'POST'])
def sbs():
    return render_template("index_sbs.html", rows=rows)


@app.route('/yhnews', methods=['GET', 'POST'])
def yhnews():
    return render_template("index_yhnews.html", rows=rows)


@app.route('/jtbc', methods=['GET', 'POST'])
def jtbc():
    return render_template("index_jtbc.html", rows=rows)


@app.route('/channel_a', methods=['GET', 'POST'])
def channel_a():
    return render_template("index_channel_a.html", rows=rows)


@app.route('/mbn', methods=['GET', 'POST'])
def mbn():
    return render_template("index_mbn.html", rows=rows)

if __name__ == '__main__':
    app.run()
