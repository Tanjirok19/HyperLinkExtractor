import telegram
from telegram.ext import Updater, MessageHandler, Filters

# Define a function to handle incoming messages
def extract_hyperlinks(update, context):
    message = update.message

    # Check if the message contains an image
    if message.photo:
        caption = message.caption

        # Check if the caption contains a hyperlink
        if message.caption_entities:
            new_caption = caption
            offset_shift = 0
            for entity in message.caption_entities:
                if entity.type == "text_link":
                    hyperlink_text = caption[entity.offset + offset_shift:entity.offset + entity.length + offset_shift]
                    hyperlink_url = entity.url

                    # Prepare the new caption with the extracted hyperlink text and link included
                    new_caption = new_caption.replace(hyperlink_text, f"<b>{hyperlink_text}</b> <b>{hyperlink_url}</b>\n\n")
                    offset_shift += len(f"{hyperlink_url}\n")  # Adjust offset for the next hyperlink

            # Send the updated message with the new caption, preserving the formatting
        context.bot.send_photo(chat_id='-1001604746255', photo=message.photo[-1].file_id, caption=new_caption, parse_mode='HTML')

# Create an instance of the Telegram Updater
updater = Updater("5859323972:AAG00CPOXPc1_LKMGw7DWmywlTweiMduCEo", use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the handler for extracting hyperlinks and handling messages with images
dispatcher.add_handler(MessageHandler(Filters.photo | Filters.forwarded, extract_hyperlinks))

if __name__ == "__main__":
    # Start the bot in long-polling mode
    updater.start_polling(poll_interval=0.5)
    updater.idle()
