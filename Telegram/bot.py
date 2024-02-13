"""
TBD
"""

import os
import logging
import time
import datetime
import json
import pytz
from telegram.constants import ParseMode
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

PG_DB_CONNECTION = os.environ["PG_DB_CONNECTION"]
PG_DB_NAME = os.environ["PG_DB_NAME"]
PG_DB_PORT = os.environ["PG_DB_PORT"]
PG_PASSWORD = os.environ["PG_PASSWORD"]
PG_USER = os.environ["PG_USER"]

user_data = {}  # a dict to dump user responses

with open(os.path.dirname(__file__) + "/../requests_data.json", encoding="utf-8") as f:
    requests_data = json.load(f)
    districts = {loc["name"] for loc in requests_data["locations_async"]}

# Making creating states in out conversation
(USER_CHOOSING_SCHEDULE, USER_RECEIVES_SCHEDULED_REPLY) = range(2)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def help_command(update: Update) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text(
        "First time use /start to begin conversation.\nTo restart conversation hit /cancel"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Hey! This is @RedBullTrackerBot\nTo restart conversation hit /cancel"
    )
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
    context.user_data["schedule"] = schedule_option

    # Here you can implement your logic based on the schedule_option
    # For example:
    chat_id = update.effective_chat.id
    scheduled_time = datetime.time(
        hour=13, minute=10, tzinfo=pytz.timezone("Asia/Tbilisi")
    )
    # days = (0, 1, 2, 3, 4, 5, 6)
    if schedule_option == "once":
        reply_user_timing = "Getting prices"
        context.job_queue.run_once(
            scheduled_report,
            1,
            data={
                "chat_id": chat_id,
                "schedule": schedule_option,
                "district": district_option,
            },
        )
    if schedule_option == "daily":
        reply_user_timing = f"You will be sent with prices schedule daily at {scheduled_time.hour}:{scheduled_time.minute}"
        context.job_queue.run_daily(
            scheduled_report,
            time=scheduled_time,
            data={
                "chat_id": chat_id,
                "schedule": schedule_option,
                "district": district_option,
            },
        )
    await context.bot.send_message(chat_id=chat_id, text=reply_user_timing)


#    await query.edit_message_text(text=f"Your scheduling option: {schedule_option}")


def pg_export(schedule, district):
    connect = psycopg2.connect(
        database=PG_DB_NAME,
        user=PG_USER,
        host=PG_DB_CONNECTION,
        password=PG_PASSWORD,
        port=PG_DB_PORT,
    )
    SQL_GET_TODAY = """SELECT p.product_name, p.product_price, g.venue_name, g.platform_name 
FROM products p JOIN general g ON p.product_id = g.product_id
WHERE p.created_at >= NOW() - INTERVAL '24 HOURS' AND p.location_name = %s 
ORDER BY p.product_price ASC LIMIT 10"""
    SQL_GET_DAILY = """SELECT product_name, product_price
    FROM products
    WHERE products.created_at >= NOW() - INTERVAL '24 HOURS'
    AND location_name = %s
    ORDER BY product_price ASC LIMIT 10"""
    try:
        cursor = connect.cursor()
        if schedule == "once":
            cursor.execute(SQL_GET_TODAY, (district,))
        if schedule == "daily":
            cursor.execute(SQL_GET_DAILY, (district,))
        result = cursor.fetchall()
        return result
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        connect.rollback()
        return []
    finally:
        cursor.close()
        connect.close()


async def save_selection_to_database(user_id, district):
    # For the future, to remeber users options and schedules if container restarts
    pass


async def scheduled_report(context: ContextTypes.DEFAULT_TYPE):
    # Beep the person who called this alarm:
    chat_id = context.job.data["chat_id"]
    schedule = context.job.data["schedule"]
    district = context.job.data["district"]
    # Gives list of tuples as a result
    result = pg_export(schedule, district)

    # To format our text as Markdown we need to escape all MD reserved characters
    def escape_markdown(text):
        """Escape markdown special characters with a backslash."""
        escape_chars = "_*[]()~`>#+-=|{}.!"
        return "".join(f"\\{char}" if char in escape_chars else char for char in text)

    # Declare new variables to store tuples results in and use MD escape function
    output = ""
    for details in result:
        name = (
            escape_markdown(details[0])
            .replace("Energy Drink", "")
            .replace("ენერგეტიკული", "")
            .replace("Energy Drunk", "")
            .replace("სასმელი", "")
        )
        price = escape_markdown(str(details[1]))
        venue = escape_markdown(details[2])
        platform = escape_markdown(details[3])

        output += f"*Name:* {name}\n*Price:* {price}\n*Venue:* {venue}\n*Platform:* {platform}\n\n"

    await context.bot.send_message(
        chat_id=chat_id, text=output, parse_mode=ParseMode.MARKDOWN_V2
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    context.user_data.clear()
    context.chat_data.clear()
    context.bot_data.clear()
    jobs = context.job_queue.get_jobs_by_name("scheduled_report")
    print(jobs)
    for job in jobs:
        job.schedule_removal()
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"User {update.effective_user.username} canceled the conversation.",
    )
    return await start(update, context)


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
