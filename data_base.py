import pymongo


class DataBase:

    def __init__(self):
        self.client = pymongo.MongoClient()
        self.words_base = self.client['english_words']

    def add_word(self, user_id: str, word: str) -> None:
        self.words_base[user_id].insert_one(word, 15)

