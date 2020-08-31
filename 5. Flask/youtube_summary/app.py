from flask import Flask, render_template, request
import sqlite3
import pymysql

app = Flask(__name__)

db = pymysql.connect(host='datacampus.mysql.database.azure.com',
                user='jhkwon@datacampus',
                password='datacampus12!',
                db='new_schema',
                charset='utf8')

cur = db.cursor(pymysql.cursors.DictCursor)



#home
cur.execute("SELECT * FROM new_schema.youtube ORDER BY date DESC")
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
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM new_schema.youtube WHERE host LIKE 'YTN%' ORDER BY DATE(date) DESC")
    ytnrows = cur.fetchall()
    ytnrows=ytnrows[:50]
    return render_template("index_ytn.html", rows=ytnrows)


@app.route('/kbs', methods=['GET', 'POST'])
def kbs():
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM new_schema.youtube WHERE host LIKE 'KBS%' ORDER BY DATE(date) DESC")
    kbsrows = cur.fetchall()
    kbsrows = kbsrows[:50]
    return render_template("index_kbs.html", rows=kbsrows)


@app.route('/mbc', methods=['GET', 'POST'])
def mbc():
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM new_schema.youtube WHERE host LIKE 'MBC%' ORDER BY DATE(date) DESC")
    mbcrows = cur.fetchall()
    mbcrows = mbcrows[:50]
    return render_template("index_mbc.html", rows=mbcrows)


@app.route('/sbs', methods=['GET', 'POST'])
def sbs():
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM new_schema.youtube WHERE host LIKE 'SBS%' ORDER BY DATE(date) DESC")
    sbsrows = cur.fetchall()
    sbsrows = sbsrows[:50]
    return render_template("index_sbs.html", rows=sbsrows)


@app.route('/yhnews', methods=['GET', 'POST'])
def yhnews():
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM new_schema.youtube WHERE host LIKE '연합%' ORDER BY DATE(date) DESC")
    yhrows = cur.fetchall()
    yhrows = yhrows[:50]
    return render_template("index_yhnews.html", rows=yhrows)


@app.route('/jtbc', methods=['GET', 'POST'])
def jtbc():
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM new_schema.youtube WHERE host LIKE 'JTBC%' ORDER BY DATE(date) DESC")
    jtbcrows = cur.fetchall()
    jtbcrows = jtbcrows[:50]
    return render_template("index_jtbc.html", rows=jtbcrows)


@app.route('/channel_a', methods=['GET', 'POST'])
def channel_a():
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM new_schema.youtube WHERE host LIKE '채널A%' ORDER BY DATE(date) DESC")
    charows = cur.fetchall()
    charows = charows[:50]
    return render_template("index_channel_a.html", rows=charows)


@app.route('/mbn', methods=['GET', 'POST'])
def mbn():
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM new_schema.youtube WHERE host LIKE 'MBN%' ORDER BY DATE(date) DESC")
    mbnrows = cur.fetchall()
    mbnrows = mbnrows[:50]
    return render_template("index_mbn.html", rows=mbnrows)

if __name__ == '__main__':
    app.run(host='172.30.1.17',port=5550)
