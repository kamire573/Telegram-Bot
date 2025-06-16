import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_BASE_URL = "https://jsonplaceholder.typicode.com"

#customization for the API Output 
POST_OUTPUT_CONFIG = {
    "fields": [
        {"key": "id", "label": "POST ID"},
        {"key": "title", "label": "Title", "translate": True},
        {"key": "body", "label": "Content", "translate": True},
    ],
    "link_template": "https://jsonplaceholder.typicode.com/posts/{id}",
    "format_template": "<br>{label}<br>: {value}\n"
}