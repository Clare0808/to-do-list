from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import list # 匯入 list.py 的路由處理