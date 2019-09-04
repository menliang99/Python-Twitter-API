from database import CursorFromConnectionFromPool
import json
import requests


class Twitter:

    def __init__(self, username, theme, content, label, tweet_id):
        self.username = username
        self.theme = theme
        self.content = content
        self.label = label
        self.id = tweet_id

    def __repr__(self):
        return "<Twitter {}>".format(self.content)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO twitters (username, theme, content, label) VALUES (%s, %s, %s, %s)',
                           (self.username, self.theme, self.content, self.label))

    def analyst(self):
        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': self.content})
        json_response = r.json()
        self.label = json_response['label']
