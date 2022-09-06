#from crypt import methods
#from turtle import title
from flask import Flask, render_template, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mytodo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    date_time = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno}-{self.title}'

@app.route('/', methods=["POST","GET"])
def hello_world():
    #return 'Hello, World!'
    
    if request.method == "POST":
        Title = request.form['title']
        Desc = request.form['desc']
        entrytodo = todo(title=Title, desc = Desc)
        db.session.add(entrytodo)
        db.session.commit()
        
    alltodo = todo.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route('/update/<int:sno>', methods = ["POST", "GET"])
def update(sno):
    if request.method=="POST":
        Title = request.form['title']
        Desc = request.form['desc']
        todo_up = todo.query.filter_by(sno=sno).first()
        todo_up.title = Title
        todo_up.desc = Desc
        db.session.add(todo_up)
        db.session.commit()
        return redirect('/')
    todo_up = todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo_up=todo_up)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo_del = todo.query.filter_by(sno=sno).first()
    db.session.delete(todo_del)
    db.session.commit()
    return redirect("/")
    
if __name__=="__main__":
    app.run(debug=True)