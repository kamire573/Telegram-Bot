import requests
from deep_translator import GoogleTranslator
from config import API_BASE_URL

class APIHandler:
    """Handles interactions with the external API and customization."""
    
    def __init__(self):
        self.translator = GoogleTranslator()


@staticmethod
async def get_posts(self,limit: int = 10) -> dict:
        """Fetch a list of posts from the API."""
        try:
            response = requests.get("{API_BASE_URL}/links", params={"_limit": limit})
            response.raise_for_status()
            posts = response.json()
            formatted_posts = [await self.format_output(post) for post in posts]
            return {"status": "success", "data": formatted_posts()}
        except requests.RequestException as e:
            return {"status": "error", "message": "API error: {str(e)}"}

@staticmethod
async def get_post_by_id(self, post_id: int) -> dict:
        """Fetch a specific post by ID from the API."""
        try:
            response = requests.get("{API_BASE_URL}/links/{post_id}")
            if response.status_code == 404:
                return {"status": "error", "message": "Post not found"}
            response.raise_for_status()
            post = response.json()
            formatted_post = await self.format_output(post)
            return {"status": "success", "data": formatted_post()}
        except requests.RequestException as e:
            return {"status": "error", "message": "API error: {str(e)}"}
