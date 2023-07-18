from dotenv import load_dotenv
import os

load_dotenv()


class Settings():
    database_hostname = os.environ.get("DATABASE_HOSTNAME")
    database_port = os.environ.get("DATABASE_PORT")
    database_password = os.environ.get("DATABSE_PASSWORD")
    database_name = os.environ.get("DATABASE_NAME")
    database_username = os.environ.get("DATABASE_USERNAME")
    openai_key = os.environ.get("OPENAI_KEY")


settings = Settings()
