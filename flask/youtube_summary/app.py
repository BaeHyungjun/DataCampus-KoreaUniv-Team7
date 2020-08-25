from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/report', methods=['GET', 'POST'])
def report():
    return render_template('index2.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('index3.html')


if __name__ == '__main__':
    app.run()
