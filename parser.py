from dataclasses import dataclass
from typing import List
from datetime import datetime
from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv


load_dotenv()


@dataclass
class UserPreferences:
    timezone: str


@dataclass
class User:
    username: str
    password: str
    roles: List[str]
    preferences: UserPreferences
    active: bool = True
    created_ts: float = datetime.utcnow()


client = MongoClient(os.getenv('MONGO_URI'))
db = client.get_default_database()
users_collection = db["users"]


with open("data.json", "r") as file:
    data = json.load(file)


def parse_roles(user_data):
    roles = []
    if user_data["is_user_admin"]:
        roles.append("admin")
    if user_data["is_user_manager"]:
        roles.append("manager")
    if user_data["is_user_tester"]:
        roles.append("teste")

    return roles


def convert_timestamp(timestamp_str):
    dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
    return dt.timestamp()


def insert_user(data):
    for user_data in data["users"]:
        roles = parse_roles(user_data)

        preferences = UserPreferences(timezone=user_data["user_timezone"])

        user = User(
            username=user_data["user"],
            password=user_data["password"],
            roles=roles,
            preferences=preferences,
            active=user_data.get("is_user_active", True),
            created_ts=convert_timestamp(user_data['created_at']) if 'created_at' in user_data else datetime.utcnow().timestamp(),
        )

        user_dict = user.__dict__
        user_dict["preferences"] = user.preferences.__dict__

        users_collection.insert_one(user_dict)


insert_user(data)