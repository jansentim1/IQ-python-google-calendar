from pathlib import Path
from dotenv import load_dotenv
from typing import Union
import logging, os


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Config(object):
    def __init__(self):
        # TODO: the app dir seems to be the root dir an de root dir is one higher
        self.APP_DIR = Path(__file__).parent
        self.ROOT_DIR = self.APP_DIR.parent

        # auth
        self.HAPIKEY: str = os.environ.get("HAPIKEY", "")
        self.CLIENT_ID: str = os.environ.get("CLIENT_ID", "")
        self.CLIENT_SECRET: str = os.environ.get("CLIENT_SECRET", "")
        self.REFRESH_TOKEN: str = os.environ.get("REFRESH_TOKEN", "")

        # mongo
        self.MONGO_COLLECTION_NAME: str = os.environ.get("MONGO_COLLECTION_NAME", "platform-users")
        self.MONGO_CLUSTER_USER: str
        self.MONGO_CLUSTER_PASS: str
        self.MONGO_CLUSTER_HOST: str
        self.MONGO_CLUSTER_URI: str


class ProdConfig(Config):
    def __init__(self):
        super().__init__()
        logging.getLogger().setLevel(logging.INFO)
        self.ENV = "prod"

        # this will break if ENV vars not provided
        self.MONGO_CLUSTER_USER: str = os.environ.get("MONGO_PROD_CLUSTER_USER")
        self.MONGO_CLUSTER_PASS: str = os.environ.get("MONGO_PROD_CLUSTER_PASS")
        self.MONGO_CLUSTER_HOST: str = os.environ.get("MONGO_PROD_CLUSTER_HOST")
        self.MONGO_CLUSTER_URI: str = (
            "mongodb+srv://" + self.MONGO_CLUSTER_USER + ":" + self.MONGO_CLUSTER_PASS + "@" + self.MONGO_CLUSTER_HOST
        )


class DevConfig(Config):
    def __init__(self):
        super().__init__()
        logging.getLogger().setLevel(logging.INFO)

        self.ENV = os.environ.get("ENV", "dev")

        # ability to use default values for development
        self.MONGO_CLUSTER_USER: str = os.environ.get("MONGO_DEV_CLUSTER_USER", "testuser")
        self.MONGO_CLUSTER_PASS: str = os.environ.get("MONGO_DEV_CLUSTER_PASS", "testpass")
        self.MONGO_CLUSTER_HOST: str = os.environ.get("MONGO_DEV_CLUSTER_HOST", "localhost")
        self.MONGO_CLUSTER_URI: str = (
            "mongodb+srv://" + self.MONGO_CLUSTER_USER + ":" + self.MONGO_CLUSTER_PASS + "@" + self.MONGO_CLUSTER_HOST
        )


config: Union[ProdConfig, DevConfig]
if os.environ.get("ENV") == "dev":
    config = DevConfig()
else:
    config = ProdConfig()
