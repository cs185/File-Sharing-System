from flask import Flask, render_template, redirect, request, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from form import RegistrationForm
import os
import userdb_models
from User_model import User
from File_model import File, Subject
from Goods_model import Goods
from Shen import cut_ext

app = Flask(__name__)
app.secret_key = 'ewpnigpewji3rwpngkps'
app.config['UPLOAD_FOLDER'] = 'C:/Users/45138/PycharmProjects/Hermes/uploads'


math = Subject('math', 'db/math.sqlite3')
TOFEL = Subject('TOFEL', 'db/TOFEL.sqlite3')
IELTS = Subject('IELTS', 'db/IELTS.sqlite3')
info101 = Subject('info101', 'db/info101.sqlite3')
info102 = Subject('info102', 'db/info102.sqlite3')
info151 = Subject('info151', 'db/info151.sqlite3')
CI = Subject('CI', 'db/CI.sqlite3')
CS = Subject('CS', 'db/CS.sqlite3')
psychology = Subject('psychology', 'db/psychology.sqlite3')
cognitive_psychology = Subject('cognitive_psychology', 'db/cognitive_psychology.sqlite3')
others = Subject('others', 'db/others.sqlite3')
goods = Goods('db/goods.sqlite3')

# delete subject files in each database
# math.delete()
# TOFEL.delete()
# IELTS.delete()
# info101.delete()
# info102.delete()
# info151.delete()
# CI.delete()
# CS.delete()
# psychology.delete()
# cognitive_psychology.delete()
# others.delete()

# delete goods database
# goods.delete()


math.init_db()
TOFEL.init_db()
IELTS.init_db()
info101.init_db()
info102.init_db()
info151.init_db()
CI.init_db()
CS.init_db()
psychology.init_db()
cognitive_psychology.init_db()
others.init_db()
goods.init_db()


for file_info in math.find_all():
    exec('{0} = {1}'.format(file_info['filename'],
                            'File(math, file_info["filename"], file_info["uploader"],file_info["type"], '
                            'file_info["downloads"], file_info["likes"])'))

for file_info in TOFEL.find_all():
    exec('{0} = {1}'.format(file_info['filename'],
                            'File(TOFEL, file_info["filename"], file_info["uploader"],file_info["type"], '
                            'file_info["downloads"], file_info["likes"])'))

for file_info in IELTS.find_all():
    exec('{0} = {1}'.format(file_info['filename'],
                            'File(math, file_info["filename"], file_info["uploader"],file_info["type"], '
                            'file_info["downloads"], file_info["likes"])'))

for file_info in info101.find_all():
    exec('{0} = {1}'.format(file_info['filename'],
                            'File(info101, file_info["filename"], file_info["uploader"],file_info["type"], '
                            'file_info["downloads"], file_info["likes"])'))

for file_info in info102.find_all():
    exec('{0} = {1}'.format(file_info['filename'],
                            'File(info102, file_info["filename"], file_info["uploader"],file_info["type"], '
                            'file_info["downloads"], file_info["likes"])'))

for file_info in info151.find_all():
    exec('{0} = {1}'.format(file_info['filename'],
                            'File(info151, file_info["filename"], file_info["uploader"],file_info["type"], '
                            'file_info["downloads"], file_info["likes"])'))

for file_info in CI.find_all():
    exec('{0} = {1}'.format(file_info['filename'],
                            'File(CI, file_info["filename"], file_info["uploader"],file_info["type"], '
                            'file_info["downloads"], file_info["likes"])'))

for file_info in CS.find_all():
    exec('{0} = {1}'.format(file_info['filename'],
                            'File(CS, file_info["filename"], file_info["uploader"],file_info["type"], '
                            'file_info["downloads"], file_info["likes"])'))

for file_info in psychology.find_all():
    exec('{0} = {1}'.format(file_info['filename'],
                            'File(psychology, file_info["filename"], file_info["uploader"],file_info["type"], '
                            'file_info["downloads"], file_info["likes"])'))

for file_info in cognitive_psychology.find_all():
    exec('{0} = {1}'.format(file_info['filename'],
                            'File(cognitive_psychology, file_info["filename"], file_info["uploader"],file_info["type"], '
                            'file_info["downloads"], file_info["likes"])'))

for file_info in others.find_all():
    exec('{0} = {1}'.format(file_info['filename'],
                            'File(others, file_info["filename"], file_info["uploader"],file_info["type"], '
                            'file_info["downloads"], file_info["likes"])'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.values.get('userid')
        session['userid'] = username
        password = request.values.get('userpwd')
        session['userpwd'] = password
        f = userdb_models.find_all()
        u = {}
        if len(f):
                for user_info in f:
                    u[user_info['username']] = user_info
                if session['userid'] in u.keys():
                    if session['userpwd'] == u[session['userid']]['password']:
                        user = userdb_models.find_one(session['userid'])
                        print(session['userid'])
                        global account
                        account = User(user[0], user[1], user[2], user[3], user[4])
                        print(account.username)
                        return redirect(url_for('index'))
                    else:
                        flash("Invalid username or password")
                        return redirect(url_for('login'))
                else:
                    flash("Invalid username or password")
                    return redirect(url_for('login'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate():
            user = {}
            user["username"] = request.form["username"]
            user["password"] = request.form["password"]
            user["fullname"] = request.form["fullname"]

            userdb_models.create(user)

            return redirect(url_for('login'))
        else:
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/admin')
def show_list():
    list = userdb_models.find_all()
    return render_template('user_list.html', list=list)


@app.route('/del')
def remove_user():
    username = request.args["username"]
    userdb_models.remove(username)
    list = userdb_models.find_all()
    return render_template('user_list.html', list=list)


@app.route('/personal_center')
def personal_center():
    try:
        user = userdb_models.find_one(session['userid'])
        account.username = user[0]
        account.fullname = user[1]
        account.upload_record = user[2]
        account.reward_points = user[3]
        account.purchase_record = user[4]
        return render_template('personal_center.html', username=account.username, fullname=account.fullname,
                               upload_record=account.upload_record, reward_points=account.reward_points,
                               purchase_record=account.purchase_record)
    except NameError:
        flash("you haven't login")
        return redirect(url_for('index'))


@app.route('/index', methods=['POST', 'GET'])
def index():
    math_list = math.find_all()
    TOFEL_list = TOFEL.find_all()
    IELTS_list = IELTS.find_all()
    info101_list = info101.find_all()
    info102_list = info102.find_all()
    info151_list = info151.find_all()
    CI_list = CI.find_all()
    CS_list = CS.find_all()
    psychology_list = psychology.find_all()
    cognitive_psychology_list = cognitive_psychology.find_all()
    others_list = others.find_all()
    return render_template('index.html', math_list=math_list, TOFEL_list=TOFEL_list, IELTS_list=IELTS_list,
                           info101_list=info101_list, info102_list=info102_list, info151_list=info151_list,
                           CI_list=CI_list, CS_list=CS_list, psychology_list=psychology_list,
                           cognitive_psychology_list=cognitive_psychology_list, others_list=others_list)


@app.route('/likes/<filename>', methods=["GET"])
def likes(filename):
    exec('%s.likes_plus()' % (filename))
    exec('%s.assign_reward()' % (filename))
    return redirect(url_for('index'))


@app.route('/upload_math', methods=['POST', 'GET'])
def upload_math():
    if request.method == 'POST':
        f = request.files['math']
        filename = secure_filename(f.filename)
        try:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            account.upload(filename, account.username)
            print(account.username)
            ext = filename.rsplit('.', 1)[1]
            filename = cut_ext(filename)
            filename = "F" + filename
            math.create(filename, account.username, ext)
            file_info = math.find_one(filename)
            exec("global {0}\n{0} = {1}".format(filename,
                                                'File(math, file_info[0], file_info[1],'
                                                'file_info[2], file_info[3], file_info[4])'))
            flash("upload successfully")
            return redirect('index')
        except FileNotFoundError:
            flash("No files selected")
            return redirect('index')
        except NameError:
            flash("you haven't login")
            return redirect(url_for('index'))


@app.route('/upload_TOFEL', methods=['POST', 'GET'])
def upload_TOFEL():
    if request.method == 'POST':
        f = request.files['TOFEL']
        filename = secure_filename(f.filename)
        try:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            account.upload(filename, account.username)
            ext = filename.rsplit('.', 1)[1]
            filename = cut_ext(filename)
            filename = "F" + filename
            TOFEL.create(filename, account.username, ext)
            file_info = TOFEL.find_one(filename)
            exec("global {0}\n{0} = {1}".format(filename,
                                                'File(TOFEL, file_info[0], file_info[1],'
                                                'file_info[2], file_info[3], file_info[4])'))
            flash("upload successfully")
            return redirect('index')
        except FileNotFoundError:
            flash("No files selected")
            return redirect('index')
        except NameError:
            flash("you haven't login")
            return redirect(url_for('index'))


@app.route('/upload_IELTS', methods=['POST', 'GET'])
def upload_IELTS():
    if request.method == 'POST':
        f = request.files['IELTS']
        filename = secure_filename(f.filename)
        try:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            account.upload(filename, account.username)
            ext = filename.rsplit('.', 1)[1]
            filename = cut_ext(filename)
            filename = "F" + filename
            IELTS.create(filename, account.username, ext)
            file_info = IELTS.find_one(filename)
            exec("global {0}\n{0} = {1}".format(filename,
                                                'File(IELTS, file_info[0], file_info[1],'
                                                'file_info[2], file_info[3], file_info[4])'))
            flash("upload successfully")
            return redirect('index')
        except FileNotFoundError:
            flash("No files selected")
            return redirect('index')
        except NameError:
            flash("you haven't login")
            return redirect(url_for('index'))


@app.route('/upload_info101', methods=['POST', 'GET'])
def upload_info101():
    if request.method == 'POST':
        f = request.files['info101']
        filename = secure_filename(f.filename)
        try:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            account.upload(filename, account.username)
            ext = filename.rsplit('.', 1)[1]
            filename = cut_ext(filename)
            filename = "F" + filename
            info101.create(filename, account.username, ext)
            file_info = info101.find_one(filename)
            exec("global {0}\n{0} = {1}".format(filename,
                                                'File(info101, file_info[0], file_info[1],'
                                                'file_info[2], file_info[3], file_info[4])'))
            flash("upload successfully")
            return redirect('index')
        except FileNotFoundError:
            flash("No files selected")
            return redirect('index')
        except NameError:
            flash("you haven't login")
            return redirect(url_for('index'))


@app.route('/upload_info102', methods=['POST', 'GET'])
def upload_info102():
    if request.method == 'POST':
        f = request.files['info102']
        filename = secure_filename(f.filename)
        try:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            account.upload(filename, account.username)
            ext = filename.rsplit('.', 1)[1]
            filename = cut_ext(filename)
            filename = "F" + filename
            info102.create(filename, account.username, ext)
            file_info = info102.find_one(filename)
            exec("global {0}\n{0} = {1}".format(filename,
                                                'File(info102, file_info[0], file_info[1],'
                                                'file_info[2], file_info[3], file_info[4])'))
            flash("upload successfully")
            return redirect('index')
        except FileNotFoundError:
            flash("No files selected")
            return redirect('index')
        except NameError:
            flash("you haven't login")
            return redirect(url_for('index'))


@app.route('/upload_info151', methods=['POST', 'GET'])
def upload_info151():
    if request.method == 'POST':
        f = request.files['info151']
        filename = secure_filename(f.filename)
        try:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            account.upload(filename, account.username)
            ext = filename.rsplit('.', 1)[1]
            filename = cut_ext(filename)
            filename = "F" + filename
            info151.create(filename, account.username, ext)
            file_info = info151.find_one(filename)
            exec("global {0}\n{0} = {1}".format(filename,
                                                'File(info151, file_info[0], file_info[1],'
                                                'file_info[2], file_info[3], file_info[4])'))
            flash("upload successfully")
            return redirect('index')
        except FileNotFoundError:
            flash("No files selected")
            return redirect('index')
        except NameError:
            flash("you haven't login")
            return redirect(url_for('index'))


@app.route('/upload_CI', methods=['POST', 'GET'])
def upload_CI():
    if request.method == 'POST':
        f = request.files['CI']
        filename = secure_filename(f.filename)
        try:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            account.upload(filename, account.username)
            ext = filename.rsplit('.', 1)[1]
            filename = cut_ext(filename)
            filename = "F" + filename
            CI.create(filename, account.username, ext)
            file_info = CI.find_one(filename)
            exec("global {0}\n{0} = {1}".format(filename,
                                                'File(CI, file_info[0], file_info[1],'
                                                'file_info[2], file_info[3], file_info[4])'))
            flash("upload successfully")
            return redirect('index')
        except FileNotFoundError:
            flash("No files selected")
            return redirect('index')
        except NameError:
            flash("you haven't login")
            return redirect(url_for('index'))


@app.route('/upload_CS', methods=['POST', 'GET'])
def upload_CS():
    if request.method == 'POST':
        f = request.files['CS']
        filename = secure_filename(f.filename)
        try:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            account.upload(filename, account.username)
            ext = filename.rsplit('.', 1)[1]
            filename = cut_ext(filename)
            filename = "F" + filename
            CS.create(filename, account.username, ext)
            file_info = CS.find_one(filename)
            exec("global {0}\n{0} = {1}".format(filename,
                                                'File(CS, file_info[0], file_info[1],'
                                                'file_info[2], file_info[3], file_info[4])'))
            flash("upload successfully")
            return redirect('index')
        except FileNotFoundError:
            flash("No files selected")
            return redirect('index')
        except NameError:
            flash("you haven't login")
            return redirect(url_for('index'))


@app.route('/upload_psychology', methods=['POST', 'GET'])
def upload_psychology():
    if request.method == 'POST':
        f = request.files['psychology']
        filename = secure_filename(f.filename)
        try:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            account.upload(filename, account.username)
            ext = filename.rsplit('.', 1)[1]
            filename = cut_ext(filename)
            filename = "F" + filename
            psychology.create(filename, account.username, ext)
            file_info = psychology.find_one(filename)
            exec("global {0}\n{0} = {1}".format(filename,
                                                'File(psychology, file_info[0], file_info[1],'
                                                'file_info[2], file_info[3], file_info[4])'))
            flash("upload successfully")
            return redirect('index')
        except FileNotFoundError:
            flash("No files selected")
            return redirect('index')
        except NameError:
            flash("you haven't login")
            return redirect(url_for('index'))


@app.route('/upload_cognitive_psychology', methods=['POST', 'GET'])
def upload_cognitive_psychology():
    if request.method == 'POST':
        f = request.files['cognitive_psychology']
        filename = secure_filename(f.filename)
        try:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            account.upload(filename, account.username)
            ext = filename.rsplit('.', 1)[1]
            filename = cut_ext(filename)
            filename = "F" + filename
            cognitive_psychology.create(filename, account.username, ext)
            file_info = cognitive_psychology.find_one(filename)
            exec("global {0}\n{0} = {1}".format(filename,
                                                'File(cognitive_psychology, file_info[0], file_info[1],'
                                                'file_info[2], file_info[3], file_info[4])'))
            flash("upload successfully")
            return redirect('index')
        except FileNotFoundError:
            flash("No files selected")
            return redirect('index')
        except NameError:
            flash("you haven't login")
            return redirect(url_for('index'))


@app.route('/upload_others', methods=['POST', 'GET'])
def upload_others():
    if request.method == 'POST':
        f = request.files['others']
        filename = secure_filename(f.filename)
        try:
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            account.upload(filename, account.username)
            ext = filename.rsplit('.', 1)[1]
            filename = cut_ext(filename)
            filename = "F" + filename
            others.create(filename, account.username, ext)
            file_info = others.find_one(filename)
            exec("global {0}\n{0} = {1}".format(filename,
                                                'File(others, file_info[0], file_info[1],'
                                                'file_info[2], file_info[3], file_info[4])'))
            flash("upload successfully")
            return redirect('index')
        except FileNotFoundError:
            flash("No files selected")
            return redirect('index')
        except NameError:
            flash("you haven't login")
            return redirect(url_for('index'))


@app.route('/download/<filename>/<type>', methods=["GET", "POST"])
def download(filename, type):
    exec('{0}.downloads_plus()' .format(filename))
    exec('{0}.assign_reward()'.format(filename))
    dirpath = "uploads"
    filename = filename.strip('F') + '.' + type
    return send_from_directory(dirpath, filename, as_attachment=True)


@app.route("/store", methods=['POST', 'GET'])
def store():
    list = goods.find_all()
    print(list)
    return render_template('store.html', list=list)


@app.route("/store/<goods_name>", methods=['POST', 'GET'])
def buy(goods_name):
    price = goods.find_price(goods_name)
    if account.reward_points >= price:
        account.buy(goods_name)
        goods.sell(goods_name, account.username)
        flash('purchase successfully')
    else:
        flash('not enough reward points')
    return redirect(url_for('store'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=True)
