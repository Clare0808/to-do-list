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

@api_bp.route("/login", methods=["GET"])
def login():
    infos = Login.query.all()  # 取得所有使用者資訊

    data_list = [{"username": info.username, "mail": info.mail, "password": info.password} for info in infos]

    return jsonify({"data": data_list}), 200  # 回傳使用者資訊列表給前端