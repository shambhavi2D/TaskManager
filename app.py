from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///task.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Todo(db.Model):
  sno = db.Column(db.Integer, primary_key=True)
  task=db.Column(db.String(200), nullable=False)
  desc = db.Column(db.String(500), nullable=False)
  date=db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self)  -> str:
    return f"{self.sno} - {self.task}"


@app.route('/',methods=["GET","POST"]) 
def home_page():
  if request.method=="POST":
    task=request.form["task"]
    desc=request.form["desc"]
    todo=Todo(task=task,desc=desc)
    db.session.add(todo)
    db.session.commit()

  allTodo = Todo.query.all()
  return render_template('home.html',allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
  todo = Todo.query.filter_by(sno=sno).first()
  db.session.delete(todo)
  db.session.commit()
  return redirect("/")

if __name__ == "__main__":
  app.run(debug=True)
  




