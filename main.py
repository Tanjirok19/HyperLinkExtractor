import telegram
from telegram.ext import Updater, MessageHandler, Filters

# Define a function to handle incoming messages
def extract_hyperlinks(update, context):
    message = update.message

    # Check if the message is a forwarded message with a photo and caption from a channel
    if message.forward_from_chat and message.forward_from_chat.type == 'channel' and message.photo and message.caption:
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
                    new_hyperlink = f'<b>{hyperlink_text}</b>\n\n{hyperlink_url}'
                    new_caption = new_caption.replace(hyperlink_text, f"<b>{hyperlink_text}</b> <b>{hyperlink_url}</b>\n\n")
                    offset_shift += len(f"{hyperlink_url}\n")  # Adjust offset for the next hyperlink

            # Send the updated message with the new caption, preserving the formatting
            context.bot.send_photo(chat_id='-1001604746255', photo=message.photo[-1].file_id, caption=new_caption, parse_mode='HTML')


# Create an instance of the Telegram Updater
updater = Updater("6276637483:AAGGGJCgvD7datJveR99TK2ZuyC28x2wpzk", use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the handler for extracting hyperlinks using a lambda function for filtering
dispatcher.add_handler(MessageHandler(Filters.all & Filters.forwarded & Filters.photo, extract_hyperlinks))

# Start the bot
if __name__ == "__main__":
    # Start the bot in long-polling mode
    updater.start_polling()
    updater.idle()
