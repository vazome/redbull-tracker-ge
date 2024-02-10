"""
TBD
"""

import os
import logging
import time
import datetime
import pytz
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
import psycopg2

TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
user_data = {}  # a dict to dump user responses
districts = ["Dighomi Massive", "Vake"]

# Making creating states in out conversation
(
    USER_CHOOSING_SCHEDULE,
    USER_RECEIVES_SCHEDULED_REPLY,
) = range(2)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text(
        "Use /start begin with this bot.\nTo start over use /cancel"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Hey!\nThis is @RedBullTrackerBot")
    return await choose_district(update, context)


async def choose_district(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends a message with district buttons"""
    keyboard_districts = [
        [InlineKeyboardButton(district, callback_data=district)]
        for district in districts
    ]
    reply_markup_districts = InlineKeyboardMarkup(keyboard_districts)
    # Artificial responsiveness through minimal sleep timer
    time.sleep(1)
    await update.message.reply_text(
        "Please select your district:",
        reply_markup=reply_markup_districts,
    )
    return USER_CHOOSING_SCHEDULE


async def choose_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    user_response = query.data

    # Store the district selection in the context user_data for later use
    context.user_data["district"] = user_response

    # Define scheduling options buttons
    keyboard_schedule = [
        [InlineKeyboardButton("Get prices now", callback_data="once")],
        [InlineKeyboardButton("Receive daily prices report", callback_data="daily")],
    ]
    reply_markup_schedule = InlineKeyboardMarkup(keyboard_schedule)

    # Edit the message to show scheduling options instead
    await query.edit_message_text(
        text=f"You selected {user_response}. How do you want to proceed with the pricing information?",
        reply_markup=reply_markup_schedule,
    )

    return USER_RECEIVES_SCHEDULED_REPLY


async def schedule_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    district_option = context.user_data["district"]
    schedule_option = query.data  # This will be either "once" or "daily"

    # Here you can implement your logic based on the schedule_option
    # For example:
    chat_id = update.effective_chat.id
    scheduled_time = datetime.time(
        hour=20, minute=59, tzinfo=pytz.timezone("Asia/Tbilisi")
    )
    # days = (0, 1, 2, 3, 4, 5, 6)
    if schedule_option == "once":
        reply_user_timing = "Getting your price now"
        context.job_queue.run_once(
            callback_alarm,
            1,
            data={"chat_id": update.effective_chat.id},
            chat_id=chat_id,
        )
    if schedule_option == "daily":
        reply_user_timing = f"You will be sent with prices schedule daily at {scheduled_time.hour}:{scheduled_time.minute}"
        context.job_queue.run_daily(
            callback_alarm,
            time=scheduled_time,
            data={"chat_id": update.effective_chat.id},
            chat_id=chat_id,
        )
    await context.bot.send_message(chat_id=chat_id, text=reply_user_timing)
    await query.edit_message_text(text=f"Your scheduling option: {schedule_option}")
    # This should end the conversation or transition to another state as needed


async def save_selection_to_database(user_id, district):
    # Implement the database insertion logic here
    # This will involve connecting to your database and inserting the data
    pass


async def callback_alarm(context: ContextTypes.DEFAULT_TYPE):
    # Beep the person who called this alarm:
    chat_id = context.job.data["chat_id"]
    await context.bot.send_message(chat_id=chat_id, text="BEEP!")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    chat_id = update.message.chat_id
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"User {update.effective_user.username} canceled the conversation.",
    )
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TG_BOT_TOKEN).build()
    convo_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            USER_CHOOSING_SCHEDULE: [CallbackQueryHandler(choose_schedule)],
            USER_RECEIVES_SCHEDULED_REPLY: [CallbackQueryHandler(schedule_chosen)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(convo_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
