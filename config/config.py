import os
from dotenv import load_dotenv

load_dotenv()

token_trello = os.getenv("token")

key_trello = os.getenv("key")

url_trello = "https://api.trello.com/1"

body_main = {
    'key': key_trello,
    'token': token_trello
}

credentials = f"key={key_trello}&token={token_trello}"

abs_path = os.path.abspath(__file__ + "../../../")

org_id = os.getenv("organization_id")

