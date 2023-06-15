import logging
import os
import time
from telegram.ext import Updater, MessageHandler, Filters
import requests
from io import BytesIO

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.getenv('6276637483:AAGGGJCgvD7datJveR99TK2ZuyC28x2wpzk')


def extract_hyperlinks(update, context):
    message = update.message
    entities = message.parse_entities(types=['url'])
    for entity in entities:
        url = entity["url"]
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Extract photo and caption from the response
                photo_file_id = BytesIO(response.content)
                new_caption = f"<a href='{url}'>{url}</a>"
                context.bot.send_photo(chat_id='-1001604746255', photo=photo_file_id, caption=new_caption, parse_mode='HTML')
        except requests.exceptions.RequestException as e:
            logger.error(f"Error extracting hyperlinks: {e}")
        except telegram.error.RetryAfter as e:
            logger.warning(f"Flood control exceeded. Retrying in {e.retry_after} seconds...")
            time.sleep(e.retry_after)
            context.bot.send_photo(chat_id='-1001604746255', photo=photo_file_id, caption=new_caption, parse_mode='HTML')


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the extract_hyperlinks handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, extract_hyperlinks))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
