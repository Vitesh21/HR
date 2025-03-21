import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    DEFAULT_WORD_COUNT = 2000
    DEFAULT_LANGUAGE = "en"