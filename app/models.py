from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(self.password)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User|username>"

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save_user(self):
        db.session.commit()
    
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

