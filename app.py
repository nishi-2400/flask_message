from flask import Flask, render_template, url_for, request
from pprint import pprint

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html', title="Index with Jinja!", msg="Jinja template")


@app.route('/',  methods=['POST'])
def form():
    ck = request.form.get('check')
    rd = request.form.get('radio')
    sel = request.form.getlist('sel')

    pprint(ck)
    return render_template('index.html', title="FORM", msg=[ck, rd, sel])


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
