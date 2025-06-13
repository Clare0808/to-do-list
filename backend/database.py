from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"  # 設定資料庫 URI
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()