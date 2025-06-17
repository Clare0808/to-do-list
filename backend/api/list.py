from flask import request, jsonify
from database import db
from . import api_bp
from models.list import Tasks

# 新增與接收任務
@api_bp.route("/list", methods=["GET", "POST"])
def get_task():
    if request.method == "POST" :
        data = request.get_json() # 獲取前端傳來的 JSON 資料並轉成 dict
        
        # 取得任務內容與類型
        task_content = data.get("task")
        task_type = data.get("task_type")

        new_task = Tasks(task=task_content, task_type=task_type) # 建立新的任務
        
        # 將任務存入資料庫
        db.session.add(new_task)
        db.session.commit()

        return jsonify({"message": "已存入資料庫"}), 201 # 回傳狀態碼

# 查詢所有任務並回傳給前端
@api_bp.route("/list/history", methods=["GET"])
def send_task():
    tasks = Tasks.query.all() # 取得所有任務

    tasks_list = [{"task_id": task.task_id, "task": task.task, "task_type": task.task_type} for task in tasks]

    return jsonify({"tasks": tasks_list}), 200 # 回傳任務列表給前端

# 刪除任務
@api_bp.route("/list/delete", methods=["POST"])
def delete_task():
    data = request.get_json()
    task_id = data.get("taskId")

    if not task_id:
        return jsonify({"error": "缺少 taskId"}), 400

    task = Tasks.query.get(task_id) # 根據 task_id 查找任務

    if not task:
        return jsonify({"error": "任務不存在"}), 404

    # 從資料庫中刪除任務
    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "任務已刪除"}), 200

# 更新任務列表
@api_bp.route("/list/update", methods=["POST"])
def update_task():
    data = request.get_json()
    task_id = data.get("task_id")
    task_type = data.get("task_type")

    task = Tasks.query.get(task_id)

    task.task_type = task_type # 修改任務類型
    db.session.commit() # 更新資料庫

    return jsonify({"message": "任務已更新"}), 200