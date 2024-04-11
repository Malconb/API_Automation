import json
from config.config import board_id, key_trello, token_trello, url_trello, body_main

with open(body_main, 'r+') as f:
    dic = json.load(f)
    dic.update({'color': 'green'})
    print(json.dump(dic, f)

          )
