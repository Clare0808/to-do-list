from flask import request, jsonify
from database import db
from . import api_bp
from models.login import Login

@api_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    mail = data.get("mail")
    password = data.get("password")

    new_log = Login(username=username, mail=mail, password=password) # 建立新的任務
        
    # 將任務存入資料庫
    db.session.add(new_log)
    db.session.commit()

    print("已存入資料庫: ", username, mail, password)

    return jsonify({"message": "已存入資料庫"}), 201 # 回傳狀態碼
