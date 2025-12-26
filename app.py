from flask import Flask, render_template,request,redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)

#SQLAlchemy.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskdatabase.db" 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #Do not keep db sessions across users.
db = SQLAlchemy(app)

#Data Model.
class MyTask(db.Model): #template for a row in the task database.
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"Task {self.id}"

with app.app_context(): #create database.
        db.create_all()

#Route to homepage.
@app.route("/",methods=["POST","GET"])
def index():
    #Add a task.
    if request.method == "POST":
        current_task = request.form["content"] #content is an input field in the form defined in html.
        new_Task = MyTask(content=current_task)
        try:
            db.session.add(new_Task)
            db.session.commit()
            return redirect("/") #reload.
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    #See all current tasks.
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks) #pass tasks to html

#Delete an item.
@app.route("/delete/<int:id>") #check html
def delete(id:int):
    task_to_delete = MyTask.query.get_or_404(id) #return item ir return 404 if not found.
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    

#Update an item.
@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id:int):
    task_to_update = MyTask.query.get_or_404(id)
    #print(task_to_update.id)
    if request.method=="POST":
        task_to_update.content = request.form["content"]
        print("updated")
        #print(task_to_update.content)
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    else:
        return render_template("update.html", task=task_to_update)
    


if __name__ == "__main__":
    app.run(debug=True)