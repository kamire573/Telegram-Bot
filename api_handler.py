import requests
from googletrans import Translator
from config import API_BASE_URL, POST_OUTPUT_CONFIG

class APIHandler:
    """Handles interactions with the external API and customization."""
    
    def __init__(self):
        self.translator = Translator()

async def translate_text(self, text: str, dest: str = "en") -> str:
        """Translate text to the specified language."""
        try:
            translated = self.translator.translate(text, dest=dest)
            return translated.text
        except Exception as e:
            return text  # Fallback to original text if translation fails

async def format_output(self, post: dict) -> str:
        """Format post data according to the output configuration."""
        output = ""
        for field in POST_OUTPUT_CONFIG["fields"]:
            value = post.get(field["key"], "")
            if field.get("translate", False):
                value = await self.translate_text(value)
            if field["key"] == "id" and POST_OUTPUT_CONFIG.get("link_template"):
                value = f'<a href="{POST_OUTPUT_CONFIG["link_template"].format(id=value)}">{value}</a>'
            output += POST_OUTPUT_CONFIG["format_template"].format(
                label=field["label"], value=value
            )
        return output

@staticmethod
async def get_posts(self,limit: int = 5) -> dict:
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