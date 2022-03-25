import pymongo

from app.config import config
from app.logging import log


def start_db(current_config):
    try:
        db_uri = current_config.MONGO_CLUSTER_URI
        db_conn = pymongo.MongoClient(db_uri, tz_aware=True)
        db = db_conn[current_config.MONGO_COLLECTION_NAME]
        log.info(f"You are running the following db: {db}")
        return db
    # TODO: catch specific exceptions
    except Exception as e:
        log.critical(f"Could not connect to {current_config.ENV.upper()} database! Error: {e}")
        log.critical(f"Exiting")
        exit(1)


db = start_db(config)
