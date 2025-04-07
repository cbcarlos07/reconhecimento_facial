from flask import app
from flask_migrate import Migrate
from config.database.models import db
from config.database.config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)