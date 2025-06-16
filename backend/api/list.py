from flask import request, jsonify
from database import db
from . import api_bp
from models.list import Tasks

@api_bp.route("/list", methods=["GET", "POST"])
def get_task():
    if request.method == "POST" :
        data = request.get_json() # 獲取前端傳來的 JSON 資料並轉成 dict
        print(f"收到前端資料: {data}")
   
        task_content = data.get("task")
        task_type = data.get("task_type")

        new_task = Tasks(task=task_content, task_type=task_type)
        db.session.add(new_task)
        db.session.commit()

        return jsonify({"message": "已存入資料庫"}), 201

@api_bp.route("/list/history", methods=["GET"])
def send_task():
    tasks = Tasks.query.all()

    tasks_list = [{"task_id": task.task_id, "task": task.task, "task_type": task.task_type} for task in tasks]

    print("所有任務:", tasks_list)

    return jsonify({"tasks": tasks_list}), 200

@api_bp.route("/list/delete", methods=["POST"])
def delete_task():
    data = request.get_json()
    task_id = data.get("taskId")

    if not task_id:
        return jsonify({"error": "缺少 taskId"}), 400

    task = Tasks.query.get(task_id)

    if not task:
        return jsonify({"error": "任務不存在"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "任務已刪除"}), 200

@api_bp.route("/list/update", methods=["POST"])
def update_task():
    data = request.get_json()
    task_id = data.get("task_id")
    task_type = data.get("task_type")

    task = Tasks.query.get(task_id)

    task.task_type = task_type
    db.session.commit()

    return jsonify({"message": "任務已更新"}), 200