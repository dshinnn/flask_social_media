from app import app
from flask_sqlalchemy import SQLAlchemy

app.config.from_object(Config)
db = SQLAlchemy(app)

from . import routes