"""
TBD
"""

import os
import logging
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
user_data = {}  # a dict to dump user responses
districts = {
    "Mtatsminda District": [
        "Mtatsminda",
        "Sololaki",
        "Vera",
        "Kiketi",
        "Kojori",
        "Shindisi",
        "Tsavkisi",
        "Tabakhmela",
        "Oqrokana",
    ],
    "Vake District": [
        "Vake",
        "Bagebi",
        "Vazha Pshavela Quarters",
        "Tskneti",
        "Nutsubidze Plato",
    ],
    "Saburtalo District": [
        "Delisi",
        "Vedzisi",
        "Vashlijvari",
        "Bakhtrioni",
        "Khiliani",
        "Didi Dighomi",
        "Zurgovana",
    ],
    "Krtsanisi District": ["Kala", "Ortachala", "Ponichala"],
    "Isani District": [
        "Avlabari",
        "Navtlughi",
        "Metromsheni",
        "Vazisubani",
        "Eighth Legioni",
    ],
    "Samgori District": [
        "Varketili",
        "Third Array",
        "Orkhevi",
        "Dampalo",
        "Lilo",
        "Lower Samgori",
    ],
    "Chughureti District": ["Chughureti", "Kukia", "Svanetisubani"],
    "Didube District": ["Didube", "Dighomi Massive"],
    "Nadzaladevi District": [
        "Nadzaladevi",
        "Sanzona",
        "Temka",
        "Lotkini",
        "Old Nadzaladevi",
    ],
    "Gldani District": ["Gldani Massive", "Avchala", "Mukhiani", "Gldanula"],
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with buttons"""
    keyboard = [
        [InlineKeyboardButton(district, callback_data=district)]
        for district in districts.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hey! This is @RedBullTrackerBot, please select you district",
    )
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def district_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    callback_data = query.data
    user_id = str(
        query.from_user.id
    )  # Convert user ID to string to use as a dictionary key

    # If the "Back" button is pressed, show the district selection again
    if "back:districts" == callback_data:
        keyboard = [
            [InlineKeyboardButton(district, callback_data=district)]
            for district in districts.keys()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # You can choose to either edit the message or send a new one
        await query.edit_message_text(
            text="Please choose a district:", reply_markup=reply_markup
        )
        return  # End the function here after handling the "Back" action

    # If a district is chosen, show the neighborhoods in that district
    if callback_data in districts:
        keyboard = [[InlineKeyboardButton("← Back", callback_data="back:districts")]]
        keyboard.extend(
            [
                InlineKeyboardButton(
                    neighborhood, callback_data=f"{callback_data}:{neighborhood}"
                )
            ]
            for neighborhood in districts[callback_data]
        )
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"Please choose a neighborhood in {callback_data}:",
            reply_markup=reply_markup,
        )
    else:
        # Simply put, the callback_data received from the user must have both district and neighborhood
        # With below section I split the string into a list the string is presented as district:neighborhood
        # Then I unpack the list into variables for better representation in the message
        # We save user provided data in user_data nested dictionary
        # And wait for the script to change the chat message with await keyword
        parts = callback_data.split(":")
        if len(parts) == 2:
            district, neighborhood = parts
            user_data[user_id] = {"district": district, "neighborhood": neighborhood}
            await query.edit_message_text(
                text=f"You selected {neighborhood} in {district}.\n{user_data}"
            )
            # Here you can add your logic to handle the user's neighborhood selection
            await save_selection_to_database(user_id, district, neighborhood)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text(
        "Use /start begin with this bot.\nYou will be presented district selection.\nTo change your choice use /edit"
    )


async def save_selection_to_database(user_id, district, neighborhood):
    # Implement the database insertion logic here
    # This will involve connecting to your database and inserting the data
    pass


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TG_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(district_chosen))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
