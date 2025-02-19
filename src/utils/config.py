from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    API_TOKEN = os.getenv("OPERATIONS_API_TOKEN")
    API_BASE_URL = os.getenv("API_BASE_URL")

    @classmethod
    def get_headers(cls):
        return {
            "Content-Type": "application/json",
            "Authorization": cls.API_TOKEN
        }
