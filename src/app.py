from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

    def serialize(self):
        return{
            "Title": self.title, 
        }

todos = [ { "label": "My first task", "done": False } ]


@app.route('/todos', methods=['GET', 'POST'])
def create_todo():

    if request.method =='GET':
        return jsonify(todos)

    if request.method =='POST':
        label = request.json.get('label')
        done = request.json.get('done')
        todos.append({"label": label, "donde": done })
        return jsonify("agregado")

@app.route('/todos/<int:position>', methods=['DELETE'])
def deleteTodo(position):
  todos.pop(position)
  return jsonify('eliminado')

#Hacia abajo tarea realizada siguiendo tutorial de internet -- arriba se encuentra lo solicitado por el bootcamp

@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)