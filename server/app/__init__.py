from config import Config
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.config.from_object(Config)


CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)


client = PyMongo(app, uri=Config.MONGO_URI)
db = client.db


from app import routes