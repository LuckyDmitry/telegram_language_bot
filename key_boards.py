from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard_part_of_speech():
    keyboard = [
            [InlineKeyboardButton("Noun", callback_data='noun'),
             InlineKeyboardButton("Verb", callback_data='verb')],
            [InlineKeyboardButton("Adverb", callback_data='adverb'),
             InlineKeyboardButton("Adjective", callback_data='adjective')],
            [InlineKeyboardButton("Nothing", callback_data='nothing')]

        ]
    return InlineKeyboardMarkup(keyboard)