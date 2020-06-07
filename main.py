import logging
from setup import TOKEN, PROXY
from telegram import Bot, Update, Message
from telegram.ext import CallbackContext, Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from process_words import WordHandler
from key_boards import keyboard_part_of_speech

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

bot = Bot(
        token=TOKEN,
        base_url=PROXY
     )

handler = WordHandler()


def start_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(f"I'm an english bot")


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Just send word and I'll remember that."
                              "Also you'll get meaning of this word")


def word_handle(update: Update, context: CallbackContext) -> None:
    word = str(update.message.text).lower().strip()
    handler.set_word(word=word)
    update.message.reply_text(handler.get_translate())
    global message_id
    message_id = update.message.reply_text(text='Please choose:',
                                           reply_markup=keyboard_part_of_speech())


def button_handler(update: Update, context=CallbackContext):  # Gets callback_data from the pushed button
    query = update.callback_query  # Gets query from callback
    button = query.data  # callback_data of pushed button
    if button == 'nothing':
        bot.delete_message(chat_id=update.effective_message.chat_id,
                           message_id=message_id.message_id)
    else:
        list_of_meanings = handler.get_meaning(button)
        if not list_of_meanings[0] == '':
            ans = ''
            for meaning, idx in zip(list_of_meanings, range(1, 6)):
                ans += str(idx) + ') ' + meaning + '\n'
        else:
            ans = 'Meaning for this part of speech doesn\'t exist'

        bot.send_message(text=ans, chat_id=update.effective_message.chat_id)


def main():

    updater = Updater(bot=bot, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start_command))
    updater.dispatcher.add_handler(CommandHandler('help', start_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, word_handle))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=button_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()
