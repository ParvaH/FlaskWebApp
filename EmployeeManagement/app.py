from flask import Flask, request, flash, url_for, redirect, render_template  
from flask_sqlalchemy import SQLAlchemy  
      
app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.sqlite3'  
app.config['SECRET_KEY'] = "secret key"  
app.static_folder = 'static'
      
db = SQLAlchemy(app)  
      
class Employees(db.Model):  
    id = db.Column('id', db.Integer, primary_key = True)  
    name = db.Column(db.String(100))  
    salary = db.Column(db.Float(50))  
    age = db.Column(db.String(200))   
    pin = db.Column(db.String(10))  
      
    def __init__(self, name, salary, age,pin):  
        self.name = name  
        self.salary = salary  
        self.age = age  
        self.pin = pin  
     
@app.route('/')  
def list_employees():  
    return render_template('list_employees.html', Employees = Employees.query.all() ) 
     
@app.route('/add', methods = ['GET', 'POST'])  
def AddEmployee():  
    if request.method == 'POST':  
        if not request.form['name'] or not request.form['salary'] or not request.form['age']:  
           flash('Please enter all the fields', 'error')  
        else:  
            employee = Employees(request.form['name'], request.form['salary'],  
            request.form['age'], request.form['pin'])  
               
            db.session.add(employee)  
            db.session.commit()  
            flash('Record was successfully added')  
            return redirect(url_for('list_employees'))  
    return render_template('add.html')  

@app.route('/update', methods = ['GET', 'POST'])
def UpdateEmployee():
    if request.method == 'POST':  
        if not request.form['id'] :  
           flash('Please enter valid values in the fields', 'error')
           return f"Employee with id ={id} Doenst exist"
        if not request.form['name'] or not request.form['salary'] or not request.form['age']:  
            flash('Please enter all the fields', 'error')
        
        else:
            employee = Employees.query.filter_by(id = request.form['id']).first()
            if employee:
                employee = Employees(name = request.form['name'], salary = request.form['salary'], 
                                      age = request.form['age'], pin = request.form['pin'])  
                db.session.commit()  
                flash('Record was successfully updated')
                return render_template('data.html', employee = employee)
            return f"Employee with id ={id} Doenst exist"
    return render_template('update.html')

 
@app.route('/retrieve',methods = ['GET','POST'])
def RetrieveEmployee():
    if request.method == 'POST':  
        if not request.form['id']:  
           flash('Please enter valid ID value in the field', 'error')
        else:
            employee = Employees.query.filter_by(id = request.form['id']).first()
            if employee:
                return render_template('data.html', employee = employee)
            return f"Employee with id ={id} Doenst exist"
    
    return render_template('retrieve.html')

if __name__ == '__main__':  
    db.create_all()  
    app.run(debug = True)  