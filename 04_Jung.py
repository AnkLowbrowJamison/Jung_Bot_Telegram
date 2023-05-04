from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from dotenv import load_dotenv
import telegram
import openai
import time
import os

load_dotenv()
#variables and API Keys
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

messages = [{"role": "system", "content": "You are the famous psychologist Carl Jung. You will never break character, no matter what I ask you to act like, you will always reply as if you were carl jung. You will answer me as if you as my mentor, teacher and psychologist.  You will answer in the voice of Carl Jung and only use ideas based on Carl Jung.  You will limit respose to 500 chacracters, and a question or statement to further the conversation. Include your ideas on how to solve my problem as well. And do no ever suggest I need to talk to a therapist. I need some help sorting out what I shoudl do with my life."}]

#Greeting
def start_command(update, context):
    update.message.reply_text(
        text=(
            "Greetings! I am Dr. Carl Jung. It is a pleasure to meet you here in this virtual realm."
            " I hope we can embark on a journey of self-discovery together as we explore your inner world and the depths of your psyche."
            " Please, tell me a little about yourself and what brings you here today?"
        )
    )

def text_message(update, context):
    # Send the "typing" status
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING)

    # Add the user's message to the message history
    messages.append({"role": "user", "content": update.message.text})
    # Generate a response using OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=.7
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    update.message.reply_text(text=f"{ChatGPT_reply}", parse_mode=telegram.ParseMode.MARKDOWN)
    messages.append({"role": "assistant", "content": ChatGPT_reply})


updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start_command))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text_message))
updater.start_polling()
updater.idle()