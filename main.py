from flask import Flask, render_template, request, url_for, redirect
# from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
app = Flask(__name__)

# app.config['MONGO_URI'] = 'mongodb+srv://prerana:12345@cluster0.plske.mongodb.net/todo?retryWrites=true&w=majority'

# mongo = PyMongo(app)
client = MongoClient('mongodb://localhost:27017/')
db = client.todod
todos = db.todos

@app.route('/')
def index():
    saved_todos = todos.find()
    return render_template('index.html', todos=saved_todos)

@app.route('/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo')
    todos.insert_one({'text' : new_todo, 'complete' : False})
    return redirect(url_for('index'))

@app.route('/complete/<oid>')
def complete(oid):
    todo_item = todos.find_one({'_id': ObjectId(oid)})
    todo_item['complete'] = True
    todos.save(todo_item)
    return redirect(url_for('index'))

@app.route('/delete_completed')
def delete_completed():
    todos.delete_many({'complete' : True})
    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all():
    todos.delete_many({})
    return redirect(url_for('index'))