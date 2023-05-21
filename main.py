from telegram.ext import Updater, MessageHandler, Filters


# Define a function to handle incoming messages
def extract_hyperlink(update, context):
    message = update.message

    # Check if the message is a forwarded message with a photo and caption
    if message.forward_from_chat and message.photo and message.caption:
        caption = message.caption

        # Check if the caption contains a hyperlink
        if message.caption_entities:
            for entity in message.caption_entities:
                if entity.type == "text_link":
                    hyperlink_text = caption[entity.offset:entity.offset + entity.length]
                    hyperlink_url = entity.url

                    # Prepare the new caption with the extracted hyperlink text and link included
                    new_caption = f"<b>{caption}</b>\n<u><b>{hyperlink_url}</b></u>"

                    # Send the updated message with the new caption, preserving the formatting
                    context.bot.send_photo(chat_id=message.from_user.id, photo=message.photo[-1].file_id, caption=new_caption, parse_mode='HTML')

    # Check if the message is a text message with a hyperlink
    elif message.text and message.entities:
        for entity in message.entities:
            if entity.type == "text_link":
                hyperlink_text = message.text[entity.offset:entity.offset + entity.length]
                hyperlink_url = entity.url

                # Prepare the new message with the extracted hyperlink text and link included
                new_message = f"<b>{message.text}</b>\n<u><b>{hyperlink_url}</b></u>"

                # Send the updated message, preserving the formatting
                context.bot.send_message(chat_id=message.from_user.id, text=new_message, parse_mode='HTML')


# Create an instance of the Telegram Updater
updater = Updater("6068678844:AAFonkifasL94AMxc3f9BA3e4qQEVqPH5vw", use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the handler for extracting hyperlinks using a lambda function for filtering
dispatcher.add_handler(MessageHandler(Filters.all & (Filters.caption_entity("text_link") | Filters.entity("text_link")), extract_hyperlink))

# Start the bot
updater.start_polling()
