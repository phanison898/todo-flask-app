from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Tast %r>' % self.id 

@app.route('/')
def index():
    if request.method == "POST":
        input_task_name = request.form['task-input']
        new_todo_model = Todo(task_name=input_task_name)
    
        try:
            db.session.add(new_todo_model)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error occured while creating new task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)