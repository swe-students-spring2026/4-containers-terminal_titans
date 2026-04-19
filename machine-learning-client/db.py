"""MongoDB helper functions for the FocusFrame ML client."""

import os
from pymongo import MongoClient  # pylint: disable=import-error

# Default to Docker-internal hostname, but allow environment override
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongodb:27017/")
DB_NAME = os.environ.get("MONGO_DBNAME", "focusframe")


def get_client():
    """Returns a MongoClient, attempting to resolve the 'mongodb' hostname if needed."""
    try:
        # Test if the intended URI works (timeout quickly)
        test_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        test_client.admin.command("ping")
        return test_client
    except Exception:
        # If 'mongodb' fails (standard for local run), try localhost
        if "//mongodb" in MONGO_URI:
            local_uri = MONGO_URI.replace("//mongodb", "//localhost")
            print(f"Switching to local URI: {local_uri}")
            return MongoClient(local_uri)
        raise


# Collection Names
USERS_COLLECTION = "users"
SESSIONS_COLLECTION = "sessions"
SNAPSHOTS_COLLECTION = "snapshots"


def get_collection(name):
    """Return a specific MongoDB collection."""
    client = get_client()
    database = client[DB_NAME]
    return database[name]


def save_snapshot(snapshot_data):
    """Insert one analysis snapshot into the snapshots collection."""
    collection = get_collection(SNAPSHOTS_COLLECTION)
    return collection.insert_one(snapshot_data)


# Maintain backward compatibility with name 'save_record' if needed
def save_record(record):
    """Alias for save_snapshot."""
    return save_snapshot(record)
