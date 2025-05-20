from flask import Flask,request,  jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #Python 的特殊變數，讓 Flask 知道你這支檔案是「主程式」
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model): #建立一個資料表
    id = db.Column(db.Integer, primary_key=True) #id：整數，主鍵（唯一、不可重複）
    task = db.Column(db.String(100), nullable=False) #task：字串，最多 100 字，不能是空的（nullable=False）

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "API with  database is running!"

@app.route("/todos", methods=["GET"]) #路由（Route）
def get_todos():
    todos = Todo.query.all()
    return jsonify([{"id": t.id, "task": t.task} for t in todos]) #把每個任務的物件變成字典（因為 JSON 不認識 class）

@app.route("/todos", methods=["POST"])
def add_todos():
    data = request.get_json() #解析請求的JSON資料
    new_todo = Todo(task=data.get("task"))
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"id": new_todo.id, "task": new_todo.task}), 201 #回傳這筆新資料，並且加上一個 HTTP 狀態碼 201，意思是「建立成功（Created）」

@app.route("/todos/<int:todo_id>", methods=["DELETE"]) #<int:todo_id>：代表從網址取得一個整數參數（任務的 ID）
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"message":f"任務 {todo_id} 已刪除"}), 200
    return jsonify({"error":"找不到這個任務"}), 404

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todos(todo_id):
    data = request.get_json()
    todo = Todo.query.get(todo_id)
    if todo:
        todo.task = data.get("task", todo.task)
        db.session.commit()
        return jsonify({"message": f"任務{todo_id} 已更新", "todo": {"id": todo.id, "task": todo.task}})
    return jsonify ({"error": "找不到這個任務"}), 404

if __name__ == "__main__":
    app.run(debug=True)