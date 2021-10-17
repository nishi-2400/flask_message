from flask import Flask, render_template, request, session, redirect, jsonify
import pickle
from pprint import pprint

app = Flask(__name__)

# byte型でシークレットキーを格納: SESSION利用のための手続き
app.secret_key = b'radam string...'

member_data = {}
message_data = []

member_data_file = 'member_data.dat'
message_data_file = 'message_data.dat'

# load member file
try:
    with open(member_data_file, "rb") as f:
        list = pickle.load(f)
        if list != None:
            member_data = list
except:
    pass

# load message file
try:
    with open(message_data_file, "rb") as f:
        list = pickle.load(f)
        if list != None:
            message_data = list
except:
    pass


@app.route('/', methods=['GET'])
def index():
    global message_data
    return render_template('message.html', login=False, title="Messages", message="not logined", data="message_data")


@app.route('/post', methods=['POST'])
def posMsg():
    global message_data
    id = request.form.get('id')
    msg = request.form.get('comment')
    message_data.append((id, msg))

    # 25件以上でメッセージ削除
    if len(message_data) > 25:
        message_data.pop(0)

    try:
        with open(message_data_file, 'wb') as f:
            # ファイルにオブジェクトを保存する
            pickle.dump(message_data, f)
    except:
        pass
    return 'True'


@app.route('/messages', methods=['GET'])
def getMsg():
    global message_data
    return jsonify(message_data)


@app.route('/login', methods=['POST'])
def login_post():
    global member_data, message_data
    id = request.form.get('id')
    pswd = request.form.get('pass')
    if id in member_data:
        if pswd == member_data[id]:
            flg = 'True'
        else:
            flg = 'False'
    else:
        member_data[id] = pswd
        flg = 'True'

        try:
            with open(member_data_file, 'wb') as f:
                pickle.dump(member_data, f)
        except:
            pass
    return flg


@app.route('/', methods=['POST'])
def form():
    msg = request.form.get('comment')
    message_data.append((session['id'], msg))
    if len(message_data) > 25:
        message_data.pop(0)
    return redirect('/')


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', title='Login', err=False, message='IDとパスワード入力：', id='')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('id', None)
    session.pop('login')
    return redirect('/login')


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
