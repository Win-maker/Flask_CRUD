from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
# app
app = Flask(__name__)

# database
app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://postgres:toor@localhost:5432/CRUD-Flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db= SQLAlchemy(app)
app.app_context().push()

# create table
class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    email = db.Column(db.String(100), nullable=False,unique=True)
    password = db.Column(db.String(100), nullable=False)
db.create_all()

@app.route('/')
def index():
    return render_template('header.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        newUser = User(email=email, password=password)
        db.session.add(newUser)
        db.session.commit()
        return redirect('/login')
    
    return render_template('signup.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        loginUser = User.query.filter_by(email = email).first()
        if loginUser:
            return redirect('/info')    
    return render_template('login.html')

@app.route('/info', methods = ['POST', 'GET'])
def info():
        getData = User.query.all()
        return render_template('information.html', getData = getData)


@app.route('/delete/<int:id>', methods = ['POST', 'GET'])
def delete(id):
    filteredData = User.query.filter_by(id=id).first()
    db.session.delete(filteredData)
    db.session.commit()
    getData = User.query.all()
    return render_template('information.html',getData=getData)

@app.route('/edit', methods = ['POST', 'GET'])
def edit():
    return render_template('update.html')

@app.route('/update', methods=['POST', 'GET'])
def update():
    update_email = request.form['updateemail']
    update_password = request.form['updatepassword']
    old_email = request.form['email']
    getData = User.query.filter_by(email = old_email).first()
    getData.email = update_email
    getData.password = update_password
    db.session.commit()
    getData = User.query.all()
    return render_template('information.html', getData=getData)
    

        
    

if __name__ == '__main__':
    app.run()