from database import db

class Tasks(db.Model):
    __tablename__ = 'tasks'
    
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task = db.Column(db.Text, nullable=False)
    task_type = db.Column(db.Boolean, default=False)
    task_time = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Tasks {self.task_id}>'