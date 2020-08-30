from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('youtubenews.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

#home
cur.execute("SELECT * FROM youtubenews ORDER BY DATE(date) DESC")
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
    conn = sqlite3.connect('youtubenews.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM youtubenews WHERE host LIKE 'YTN%' ORDER BY DATE(date) DESC")
    ytnrows = cur.fetchall()
    ytnrows=ytnrows[:50]
    return render_template("index_ytn.html", rows=ytnrows)


@app.route('/kbs', methods=['GET', 'POST'])
def kbs():
    conn = sqlite3.connect('youtubenews.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM youtubenews WHERE host LIKE 'KBS%' ORDER BY DATE(date) DESC")
    kbsrows = cur.fetchall()
    kbsrows = kbsrows[:50]
    return render_template("index_kbs.html", rows=kbsrows)


@app.route('/mbc', methods=['GET', 'POST'])
def mbc():
    conn = sqlite3.connect('youtubenews.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM youtubenews WHERE host LIKE 'MBC%' ORDER BY DATE(date) DESC")
    mbcrows = cur.fetchall()
    mbcrows = mbcrows[:50]
    return render_template("index_mbc.html", rows=mbcrows)


@app.route('/sbs', methods=['GET', 'POST'])
def sbs():
    conn = sqlite3.connect('youtubenews.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM youtubenews WHERE host LIKE 'SBS%' ORDER BY DATE(date) DESC")
    sbsrows = cur.fetchall()
    sbsrows = sbsrows[:50]
    return render_template("index_sbs.html", rows=sbsrows)


@app.route('/yhnews', methods=['GET', 'POST'])
def yhnews():
    conn = sqlite3.connect('youtubenews.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM youtubenews WHERE host LIKE '연합%' ORDER BY DATE(date) DESC")
    yhrows = cur.fetchall()
    yhrows = yhrows[:50]
    return render_template("index_yhnews.html", rows=yhrows)


@app.route('/jtbc', methods=['GET', 'POST'])
def jtbc():
    conn = sqlite3.connect('youtubenews.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM youtubenews WHERE host LIKE 'JTBC%' ORDER BY DATE(date) DESC")
    jtbcrows = cur.fetchall()
    jtbcrows = jtbcrows[:50]
    return render_template("index_jtbc.html", rows=jtbcrows)


@app.route('/channel_a', methods=['GET', 'POST'])
def channel_a():
    conn = sqlite3.connect('youtubenews.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM youtubenews WHERE host LIKE '채널A%' ORDER BY DATE(date) DESC")
    charows = cur.fetchall()
    charows = charows[:50]
    return render_template("index_channel_a.html", rows=charows)


@app.route('/mbn', methods=['GET', 'POST'])
def mbn():
    conn = sqlite3.connect('youtubenews.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM youtubenews WHERE host LIKE 'MBN%' ORDER BY DATE(date) DESC")
    mbnrows = cur.fetchall()
    mbnrows = mbnrows[:50]
    return render_template("index_mbn.html", rows=mbnrows)

if __name__ == '__main__':
    app.run()
