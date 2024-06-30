from pymongo import MongoClient
import streamlit as st
from dotenv import load_dotenv
import os
import bcrypt
import logging
import datetime

logging.basicConfig(level=logging.DEBUG)

def get_mongo_client():
    client = MongoClient(st.secrets.MONGO_URI2)
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

def store_api(username, api_key):
    credentials = get_user_collection()
    result = credentials.update_one(
        {"username": username},
        {"$set": {"api": api_key}}
    )
    # return result.modified_count > 0

def bookmark_paper(username, paper_id, title, abstract):
    try:
        collection = get_user_collection()
        result = collection.update_one(
            {'username': username},
            {'$push': {"bookmarked_papers": {"paper_id": paper_id, "title": title, "abstract": abstract}}}
        )
        logging.debug(f'Result: {result.raw_result}')
        
    except Exception as e:
        logging.error(f'Error bookmarking paper: {e}')

def get_bookmarked_papers(username):
    collection = get_user_collection()
    user = collection.find_one({"username": username}, {"bookmarked_papers": 1, "_id": 0})
    return user.get("bookmarked_papers", []) if user else []

def add_search_history(username, query):
    collection = get_user_collection()
    collection.update_one(
        {"username": username},
        {"$push": {"search_history": {"query": query, "timestamp": datetime.datetime.utcnow()}}}
    )

def get_search_history(username):
    collection = get_user_collection()
    user = collection.find_one({"username": username}, {"search_history": 1, "_id": 0})
    return user.get("search_history", []) if user else []

def get_free_search(username):
    collection = get_user_collection()
    user = collection.find_one({'username': username})
    if "free_searches" not in user:
        collection.update_one({"username": username}, {"$set": {"free_searches": 0}})
        return 0
    
    return user["free_searches"]

def increment_free_search(username):
    collection = get_user_collection()
    collection.update_one({"username": username}, {"$inc": {"free_searches": 1}})