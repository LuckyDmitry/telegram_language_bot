import logging
import json
import os
from googletrans import Translator
from telegram import Bot, Update, Message
from telegram.ext import CallbackContext, Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

vocabulary = {}
FILE_WORDS = "words.json"


def find_meaning(word, src_l='en', dest_l='ru'):
    """"Find the meaning of word and return meaning """
    word = Translator().translate(word, src=src_l, dest=dest_l)
    return word.text


def load_words():
    global vocabulary
    if os.stat(FILE_WORDS).st_size == 0:
        return
    with open(FILE_WORDS, 'r', encoding="utf-8") as f:
        vocabulary = json.load(f)


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f"I'm an english bot")


def word_handle(update: Update, context: CallbackContext):
    dest_word = find_meaning(str(update.message.text).lower().strip())
    add_vocabulary(update.message.text, dest_word)
    update.message.reply_text(str(dest_word).lower().strip())


def add_vocabulary(src_word, dest_word):
    """Add new word in vocabulary"""
    if src_word.strip() not in vocabulary.keys():
        vocabulary[src_word.strip().lower()] = [dest_word.strip().lower(), 15]
    save_words()


def delete_word(update: Update, context: CallbackContext):
    word = str(update.message.text)[4:].strip().lower()
    if word in vocabulary.keys():
        del vocabulary[word]


def save_words():
    print(vocabulary)
    with open(FILE_WORDS, 'w+', encoding="utf-8") as f_words:
        json.dump(vocabulary, f_words, ensure_ascii=False, indent=2)


def print_vocabulary(update: Update, context: CallbackContext):
    if len(vocabulary) == 0:
        update.message.reply_text("While vocabulary is empty")
        return
    words_message = ""
    for key, value in vocabulary.items():
        words_message += f"{key} : {str(value[0]).lower().strip()}\n\n"
    update.message.reply_text(words_message)


def main():
    try:
        bot = Bot(
            token='1114504091:AAHuB_E7EKQIA6ysmfrlWKDX_EQ8NbetGuc',
            base_url='https://telegg.ru/orig/bot'
         )
        updater = Updater(bot=bot, use_context=True)

        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(CommandHandler('print', print_vocabulary))
        updater.dispatcher.add_handler(CommandHandler('del', delete_word))
        updater.dispatcher.add_handler(MessageHandler(Filters.all, word_handle))

        updater.start_polling()
        updater.idle()
    except:
        save_words()


if __name__ == '__main__':
    logger.info('Start Bot')
    load_words()
    main()
