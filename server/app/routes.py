from datetime import datetime
from bson import ObjectId
from app import app
from app import db
from flask import jsonify, request


@app.route("/")
def list_users():
    users_collection = db.users
    users = users_collection.find()

    # Convert MongoDB user documents to a list of dictionaries, extracting all fields
    user_list = []
    for user in users:
        user_data = {
            "id": str(user["_id"]),
            "username": user["username"],
            "password": user[
                "password"
            ],  # Consider not exposing passwords in production
            "roles": user["roles"],
            "preferences": {"timezone": user["preferences"]["timezone"]},
            "active": user.get("active", True),
            "created_ts": user["created_ts"],
        }
        user_list.append(user_data)

    return jsonify(user_list)


@app.route("/create-user", methods=["POST"])
def create_user():
    users_collection = db.users
    data = request.get_json()

    print(data)

    # Ensure all required fields are present in the request
    if (
        "username" not in data
        or "password" not in data
        or "roles" not in data
        or "preferences" not in data
    ):
        return jsonify({"error": "Missing required fields"}), 400

    # Prepare the new user document
    new_user = {
        "username": data["username"],
        "password": data["password"],  # Consider hashing the password in production
        "roles": data["roles"],
        "preferences": {"timezone": data["preferences"]["timezone"]},
        "active": data.get("active", True),  # Default to active if not provided
        "created_ts": datetime.utcnow().timestamp(),  # Use current timestamp
    }

    # Insert the new user into the users collection
    result = users_collection.insert_one(new_user)

    # Return the created user with their new ID
    new_user["_id"] = str(result.inserted_id)
    return jsonify(new_user), 201


@app.route("/get-user/<user_id>", methods=["GET"])
def get_user(user_id):
    users_collection = db.users

    user = users_collection.find_one({"_id": ObjectId(user_id)})

    print(user)

    user_data = {
        "id": str(user["_id"]),
        "username": user["username"],
        "password": user["password"],
        "roles": user["roles"],
        "preferences": {"timezone": user["preferences"]["timezone"]},
        "active": user.get("active", True),
        "created_ts": user["created_ts"],
    }

    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_data)


@app.route("/delete-user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    users_collection = db.users

    # Attempt to delete the user by their ObjectId
    result = users_collection.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count > 0:
        return jsonify({"message": f"User {user_id} deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@app.route("/edit-user/<user_id>", methods=["POST"])
def edit_user(user_id):
    users_collection = db.users
    data = request.get_json()

    # Prepare the updated fields based on the request payload
    update_fields = {}

    if "username" in data:
        update_fields["username"] = data["username"]
    if "password" in data:
        update_fields["password"] = data["password"]  # Consider hashing in production
    if "roles" in data:
        update_fields["roles"] = data["roles"]
    if "preferences" in data and "timezone" in data["preferences"]:
        update_fields["preferences.timezone"] = data["preferences"]["timezone"]
    if "active" in data:
        update_fields["active"] = data["active"]

    # Perform the update operation
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},  # Find the user by ID
        {"$set": update_fields},  # Update the fields
    )

    if result.matched_count > 0:
        return jsonify({"message": f"User {user_id} updated successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404
