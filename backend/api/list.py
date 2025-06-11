from api import api_bp

@api_bp.route("/list")
def get_list():
    return "get list"