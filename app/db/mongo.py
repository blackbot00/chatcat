from pymongo import MongoClient
from app.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["coupledatingbot"]

users_col = db["users"]
chats_col = db["chats"]
payments_col = db["payments"]
reports_col = db["reports"]
