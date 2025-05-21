# handlers.py
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from keyboard import get_main_menu, get_confirm_menu, get_cancel_menu
from config import ADMIN_IDS, DB_NAME
from database import Database
from localization import Localization
from logger import setup_logger
import uuid
from datetime import datetime

logger = setup_logger()
db = Database(DB_NAME)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = context.user_data.get("lang", "ru")
    await update.message.reply_text(
        Localization.get_message(update, "welcome", lang),
        parse_mode="HTML",
        reply_markup=get_main_menu(lang)
    )
    logger.info(f"User @{user.username or user.first_name} started the bot.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user = query.from_user
    user_id = user.id
    username = user.username or user.first_name
    lang = context.user_data.get("lang", "ru")

    if data.startswith("buy_"):
        stars = int(data.split("_")[1])
        order_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.add_order(order_id, user_id, username, stars, "pending", timestamp)

        user_message = Localization.get_message(
            update, "order_created", lang, order_id=order_id, stars=stars
        )
        await query.message.reply_text(
            user_message, parse_mode="HTML", reply_markup=get_cancel_menu(order_id, lang)
        )

        admin_message = Localization.get_message(
            update, "admin_new_order", lang, order_id=order_id, username=username, stars=stars, timestamp=timestamp
        )
        for admin_id in ADMIN_IDS:
            await context.bot.send_message(
                chat_id=admin_id,
                text=admin_message,
                parse_mode="HTML",
                reply_markup=get_confirm_menu(order_id, lang)
            )
        logger.info(f"Order #{order_id} created by @{username} for {stars} stars.")

    elif data.startswith("confirm_"):
        order_id = data.split("_")[1]
        order = db.get_order(order_id)
        if not order:
            await query.message.reply_text(Localization.get_message(update, "order_not_found", lang), parse_mode="HTML")
            return

        db.update_order_status(order_id, "confirmed")
        db.add_to_history(order_id, order["user_id"], order["stars"], "confirmed", order["timestamp"])
        db.delete_order(order_id)

        user_message = Localization.get_message(
            update, "order_confirmed", lang, order_id=order_id, stars=order["stars"]
        )
        await context.bot.send_message(
            chat_id=order["user_id"], text=user_message, parse_mode="HTML"
        )
        await query.message.reply_text(f"✅ Order #{order_id} confirmed.", parse_mode="HTML")
        logger.info(f"Order #{order_id} confirmed by admin.")

    elif data.startswith("reject_"):
        order_id = data.split("_")[1]
        order = db.get_order(order_id)
        if not order:
            await query.message.reply_text(Localization.get_message(update, "order_not_found", lang), parse_mode="HTML")
            return

        db.update_order_status(order_id, "rejected")
        db.add_to_history(order_id, order["user_id"], order["stars"], "rejected", order["timestamp"])
        db.delete_order(order_id)

        user_message = Localization.get_message(
            update, "order_rejected", lang, order_id=order_id, stars=order["stars"]
        )
        await context.bot.send_message(
            chat_id=order["user_id"], text=user_message, parse_mode="HTML"
        )
        await query.message.reply_text(f"❌ Order #{order_id} rejected.", parse_mode="HTML")
        logger.info(f"Order #{order_id} rejected by admin.")

    elif data.startswith("cancel_"):
        order_id = data.split("_")[1]
        order = db.get_order(order_id)
        if not order:
            await query.message.reply_text(Localization.get_message(update, "order_not_found", lang), parse_mode="HTML")
            return

        if order["user_id"] != user_id:
            await query.message.reply_text(Localization.get_message(update, "no_permission", lang), parse_mode="HTML")
            return

        db.update_order_status(order_id, "cancelled")
        db.add_to_history(order_id, order["user_id"], order["stars"], "cancelled", order["timestamp"])
        db.delete_order(order_id)

        user_message = Localization.get_message(update, "order_cancelled", lang, order_id=order_id)
        await query.message.reply_text(user_message, parse_mode="HTML")

        for admin_id in ADMIN_IDS:
            await context.bot.send_message(
                chat_id=admin_id,
                text=Localization.get_message(update, "admin_order_cancelled", lang, order_id=order_id, username=username),
                parse_mode="HTML"
            )
        logger.info(f"Order #{order_id} cancelled by @{username}.")

    elif data.startswith("details_"):
        order_id = data.split("_")[1]
        order = db.get_order(order_id)
        if not order:
            await query.message.reply_text(Localization.get_message(update, "order_not_found", lang), parse_mode="HTML")
            return

        details_message = Localization.get_message(
            update, "order_details", lang,
            order_id=order_id, username=order["username"], stars=order["stars"],
            status=order["status"], timestamp=order["timestamp"]
        )
        await query.message.reply_text(details_message, parse_mode="HTML")

    elif data == "check_status":
        orders = db.get_user_orders(user_id)
        if not orders:
            await query.message.reply_text(Localization.get_message(update, "no_orders", lang), parse_mode="HTML")
            return

        orders_text = "\n".join(
            f"Заявка #{order['order_id']} | Звезды: {order['stars']} | Статус: {order['status']} | Время: {order['timestamp']}"
            if lang == "ru" else
            f"Order #{order['order_id']} | Stars: {order['stars']} | Status: {order['status']} | Time: {order['timestamp']}"
            for order in orders
        )
        status_message = Localization.get_message(update, "status", lang, orders=orders_text)
        await query.message.reply_text(status_message, parse_mode="HTML", reply_markup=get_main_menu(lang))
        logger.info(f"User @{username} checked order status.")

    elif data == "check_history":
        history = db.get_user_history(user_id)
        if not history:
            await query.message.reply_text("📭 У вас нет истории покупок." if lang == "ru" else "📭 No purchase history.", parse_mode="HTML")
            return

        history_text = "\n".join(
            f"Заявка #{entry['order_id']} | Звезды: {entry['stars']} | Статус: {entry['status']} | Время: {entry['timestamp']}"
            if lang == "ru" else
            f"Order #{entry['order_id']} | Stars: {entry['stars']} | Status: {entry['status']} | Time: {entry['timestamp']}"
            for entry in history
        )
        history_message = Localization.get_message(update, "history", lang, history=history_text)
        await query.message.reply_text(history_message, parse_mode="HTML", reply_markup=get_main_menu(lang))
        logger.info(f"User @{username} checked purchase history.")

    elif data == "help":
        await query.message.reply_text(
            Localization.get_message(update, "help", lang),
            parse_mode="HTML",
            reply_markup=get_main_menu(lang)
        )
        logger.info(f"User @{username} accessed help.")

    elif data == "support":
        await query.message.reply_text(
            Localization.get_message(update, "support", lang),
            parse_mode="HTML",
            reply_markup=get_main_menu(lang)
        )
        logger.info(f"User @{username} accessed support.")

    elif data == "lang_switch":
        context.user_data["lang"] = "en" if lang == "ru" else "ru"
        await query.message.reply_text(
            "Язык изменен!" if lang == "ru" else "Language changed!",
            parse_mode="HTML",
            reply_markup=get_main_menu(context.user_data["lang"])
        )
        logger.info(f"User @{username} switched language to {context.user_data['lang']}.")