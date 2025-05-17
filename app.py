from flask import Flask,request,  jsonify

app = Flask(__name__) #Python 的特殊變數，讓 Flask 知道你這支檔案是「主程式」

todos = [
    {"id": 1, "task": "買早餐"},
    {"id": 2, "task": "學 Flask"},
]

@app.route("/todos", methods=["GET"]) #路由（Route）
def get_todos():
    return jsonify(todos) #把一個 Python 字典（{"message": "..."}）轉換成 JSON 格式

@app.route("/todos", methods=["POST"])
def add_todos():
    data = request.get_json() #解析請求的JSON資料
    new_todo = {
        "id": len(todos) + 1,
        "task": data.get("task") #取出 "task" 這個欄位（用 .get() 比較安全）
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201 #回傳這筆新資料，並且加上一個 HTTP 狀態碼 201，意思是「建立成功（Created）」

@app.route("/todos/<int:todo_id>", methods=["DELETE"]) #<int:todo_id>：代表從網址取得一個整數參數（任務的 ID）
def delete_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return jsonify({"message":f"任務 {todo_id} 已刪除"}), 200
    return jsonify({"error":"找不到這個任務"}), 404

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todos(todo_id):
    data = request.get_json()
    for todo in todos:
        if todo["id"] == todo_id:
            todo["task"] = data.get("task", todo["task"])
            return jsonify({"message": f"任務{todo_id}已更新", "todo":todo}), 200
    return jsonify({"message":"找不到這個任務"}), 404

if __name__ == "__main__":
    app.run(debug=True)