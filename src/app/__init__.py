from flask import Flask
import mongoengine

app = Flask(__name__)
app.config.from_object("config")
db = mongoengine

from app import views, models

