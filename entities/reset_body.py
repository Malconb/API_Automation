from config.config import key_trello, token_trello


class Body:

    def reset_body(self):
        body_main = {
            'key': key_trello,
            'token': token_trello
        }

        return body_main
