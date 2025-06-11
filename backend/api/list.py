from flask import request, jsonify
from . import api_bp

@api_bp.route("/list", methods=["GET", "POST"])
def get_task():
    if request.method == "POST" :
        data = request.get_json() # 將前端接收到的 JSON 資料轉換為 dict
        print(f"收到前端資料: {data}")

        return jsonify({"message": "資料已收到"}), 200