import certifi
from pymongo import MongoClient

MONGODB_URI = "mongodb+srv://mindsetfuel5274:V4K5txDYRW1yC5VJ@kasi.y4czfjc.mongodb.net/?retryWrites=true&w=majority&appName=kasi"
client = MongoClient(MONGODB_URI, tls=True, tlsCAFile=certifi.where())
db = client["sample_analytics"]

def get_collection_names():
    try:
        return db.list_collection_names()
    except Exception as e:
        return [f"Error: {e}"]

def get_field_names(collection):
    doc = db[collection].find_one()
    if doc:
        return list(doc.keys())
    return []

def find_in_collection(collection, query, projection=None, limit=5):
    try:
        if projection:
            # Ensure projection is a dict, not a set
            if isinstance(projection, set):
                projection = {field: 1 for field in projection}
            return list(db[collection].find(query, projection).limit(limit))
        else:
            return list(db[collection].find(query).limit(limit))
    except Exception as e:
        return [f"Error: {e}"]

def aggregate_in_collection(collection, pipeline):
    try:
        return list(db[collection].aggregate(pipeline))
    except Exception as e:
        return [f"Error: {e}"]
