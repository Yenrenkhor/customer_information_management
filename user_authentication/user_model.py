from flask_sqlalchemy import SQLAlchemy

user_db = SQLAlchemy()


class User(user_db.Model):
    __tablename__ = 'users'
    id = user_db.Column(user_db.Integer, primary_key=True)
    username = user_db.Column(user_db.String(), nullable=False)
    password = user_db.Column(user_db.String(), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
