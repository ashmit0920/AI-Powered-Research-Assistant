from pymongo import MongoClient
import streamlit as st
from dotenv import load_dotenv
import os
import bcrypt

def get_mongo_client():
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI)
    return client

def get_user_collection():
    client = get_mongo_client()
    db = client["Lucid"]  # database name
    collection = db["credentials"]  # collection name
    return collection

def register_user(username, password):
    collection = get_user_collection()
    if collection.find_one({"username": username}):
        return False  # User already exists
    
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    collection.insert_one({"username": username, "password": hash.decode('utf-8')})
    return True

def authenticate_user(username, password):
    collection = get_user_collection()
    user = collection.find_one({"username": username})
    if user:
        stored_hash = user['password'].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    return False

def list_users():
    collection = get_user_collection()
    return list(collection.find({}))
