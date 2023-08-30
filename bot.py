import os
import gpt
import responses
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()   

TOKEN = os.getenv('TOKEN') 
BOT_USERNAME = os.getenv('BOT_USERNAME')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me! I am a koala!')
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am a koala! How may I assist you?')
    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    user_message: str = update.message.text
    
    print(f'User {update.message.chat.id} in {message_type}: "{user_message}')
    
    for command in ['/ai', '/gpt']:
            if user_message.startswith(command):
                command = user_message.split(' ')[0]
                user_message = user_message.replace(user_message, '')
                response = gpt.handle_response(user_message)                
            else: 
                if message_type == "group":
                    if BOT_USERNAME in user_message:
                        user_message = user_message.replace(BOT_USERNAME, '')
                        response = responses.handle_response(user_message)
                    else:
                        return
                else:
                    print('dm chat')
                    response = responses.handle_response(user_message)
                    
    await update.message.reply_text(response) 
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    
def run_tele_bot():
    print('Starting bot...')
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    app.add_error_handler(error)
    
    app.run_polling(poll_interval=3)