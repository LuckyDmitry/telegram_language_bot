from googletrans import Translator
import requests
import re


class WordHandler:

    def __init__(self):
        self.word = str
        self.api_url = "https://twinword-word-graph-dictionary.p.rapidapi.com/definition/"
        self.headers = {'x-rapidapi-host': "twinword-word-graph-dictionary.p.rapidapi.com",
                        'x-rapidapi-key': "f59705ee70mshddcb045dff86210p10f7d0jsn1294bb09f987"}

    def set_word(self, word: str) -> None:
        self.word = word

    def get_translate(self, src_l: str = 'en', dest_l: str = 'ru') -> str:
        """"Translate word from one language into another and return result"""
        word = Translator().translate(self.word, src=src_l, dest=dest_l)
        return str(word.text).lower()

    def request_api(self) -> map:
        response = requests.request("GET", self.api_url, headers=self.headers, params={"entry": self.word})
        if response.status_code != 200:
            raise ConnectionError("Repeat later or send us this error")
        json_response = response.json()
        if json_response['result_msg'] != 'Success':
            raise ValueError("Incorrect word")
        return json_response

    def get_meaning(self, part_of_speech: str) -> list:
        response = self.request_api()
        raw_meaning = response['meaning'][part_of_speech]
        meaning = re.sub(r'[(](vrb|nou|adv|adj)[)]\s', '', raw_meaning)
        return meaning.split('\n')
