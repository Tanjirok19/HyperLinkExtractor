import telegram
from telegram.ext import Updater, MessageHandler, Filters
import re

# Define a function to handle incoming messages
def extract_hyperlinks(update, context):
    message = update.message

    # Check if the message contains an image with a caption
    if message.photo and message.caption:
        caption = message.caption

        # Extract and replace hyperlinks in the caption using regex
        hyperlink_pattern = r'<a href="(.*?)">(.*?)</a>'
        new_caption = re.sub(hyperlink_pattern, r'<b>\2</b> <b>\1</b>\n\n', caption, flags=re.IGNORECASE)

        # Send the updated message with the new caption, preserving the formatting
        photo_file_id = message.photo[-1].file_id
        context.bot.send_photo(chat_id='-1001604746255', photo=photo_file_id, caption=new_caption, parse_mode='HTML')

# Create an instance of the Telegram Updater
updater = Updater("6276637483:AAGGGJCgvD7datJveR99TK2ZuyC28x2wpzk", use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the handler for extracting hyperlinks and handling messages with images
dispatcher.add_handler(MessageHandler(Filters.photo & Filters.caption, extract_hyperlinks))

# Start the bot
if __name__ == "__main__":
    # Start the bot in long-polling mode
    updater.start_polling()
    updater.idle()
