from flask import Flask,render_template,request,redirect,session
from flask_mysqldb import MySQL,MySQLdb
from datetime import datetime
from flask_session import Session
from datetime import timedelta
app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='TODO'
app.config['SECRET_KEY']='1234'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_TIMEOUT'] = timedelta(minutes=1)


mysql=MySQL(app)
Session(app)

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        username = request.form['username']
        email=request.form['email']
        password = request.form['password']
        # gender=request.form['gender']
        mobileno=request.form['mbno']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query="INSERT INTO users (firstname,lastname,username,email,password,gender,mobileno ) VALUES (%s,%s,%s,%s,%s,'male',%s)"
        cur.execute(query, (firstname, lastname, username,email,password,mobileno  ))
        mysql.connection.commit()
        cur.close()
        session['username']=username
        return redirect('/home')
    else:
        return render_template('signuplogin.html')

@app.route('/login',methods=['POST'])
def login():
    username=request.form['username']
    password=request.form['password']
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    exists=cur.execute('SELECT password from users WHERE username=(%s)',(username,))
    if exists>0:
        realpassword=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        print(realpassword['password'])
        if realpassword['password']==password:
            print('loggin success')
            session['username']=username
            return redirect('/home')
        else:
            return redirect('/')
    else:
        return redirect('/')
@app.route('/logout')
def logout():
    session['username']=None
    return redirect('/')



# all todos home
@app.route('/home',methods=['GET','POST'])
def newtodo():
    username = session['username']
    if username!=None:
        if request.method=='POST':
            cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            title=request.form['title']
            desc=request.form['desc']
            timecreated=datetime.utcnow()
            cur.execute("INSERT INTO mytodo (username,title,description,datecreated) VALUES (%s,%s,%s,%s)",(username,title,desc,timecreated))
            mysql.connection.commit()
            cur.close()
        cur=mysql.connection.cursor()
        total=cur.execute("SELECT * FROM mytodo where username=(%s)",(username,))
        if total>0:
            todos=cur.fetchall()
            cur.close()
            return render_template('index.html', todos=todos,username=username)
        return render_template('index.html',username=username)
    else:
        return redirect('/')

@app.route('/update/<id>',methods=['POST','GET'])
def update(id):
    username = session['username']
    if  username!= None:
        if request.method=='GET':
            cur = mysql.connection.cursor()
            total=cur.execute("SELECT * FROM mytodo WHERE id = (%s);", (id,))
            if total>0:
                found=cur.fetchall()
                found=found[0]
            return render_template('update.html',found=found)
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            timecreated = datetime.utcnow()
            title = request.form['title']
            desc = request.form['desc']
            cur.execute("UPDATE mytodo SET title=(%s),description=(%s),datecreated=(%s) WHERE id=(%s)", (title, desc, timecreated,id))
            mysql.connection.commit()
            cur.close()
            return redirect('/home')
    else:
        return redirect('/')

@app.route('/delete/<x>')
def delete(x):
    username = session['username']
    if username != None:
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("DELETE FROM mytodo WHERE id=(%s)", [x,])
        mysql.connection.commit()
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/about',methods=['GET'])
def about():
    username = session['username']
    if username != None:
        return render_template('about.html',username=username)
    else:
        return redirect('/')

@app.route('/profile',methods=['GET','POST'])
def profile():
    username = session['username']
    if username != None:
        if request.method=='POST':
            pass
        else:
            return render_template('profile.html',username=username)
    else:
        return redirect('/')

@app.route('/search',methods=['POST'])
def search():
    username = session['username']
    if username != None:
        cur = mysql.connection.cursor()
        searched=request.form['search']
        total = cur.execute("SELECT * FROM mytodo where title=(%s)", (searched,))
        if total > 0:
            todos = cur.fetchall()
            cur.close()
            print(todos)
            return render_template('index.html', todos=todos, username=username)
        return render_template('index.html', username=username)

    else:
        return redirect('/')

app.run(debug=True,port=8000)
