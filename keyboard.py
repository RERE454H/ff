# keyboard.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu(lang="ru"):
    keyboard = [
        [
            InlineKeyboardButton("🌟 10", callback_data="buy_10"),
            InlineKeyboardButton("🌟 50", callback_data="buy_50"),
            InlineKeyboardButton("🌟 100", callback_data="buy_100")
        ],
        [
            InlineKeyboardButton("🌟 250", callback_data="buy_250"),
            InlineKeyboardButton("🌟 500", callback_data="buy_500"),
            InlineKeyboardButton("🌟 1000", callback_data="buy_1000")
        ],
        [
            InlineKeyboardButton("🌟 2500", callback_data="buy_2500"),
            InlineKeyboardButton("🌟 5000", callback_data="buy_5000"),
            InlineKeyboardButton("🌟 10000", callback_data="buy_10000")
        ],
        [
            InlineKeyboardButton("📋 Мои заявки" if lang == "ru" else "📋 My Orders", callback_data="check_status"),
            InlineKeyboardButton("📜 История" if lang == "ru" else "📜 History", callback_data="check_history")
        ],
        [
            InlineKeyboardButton("❓ Помощь" if lang == "ru" else "❓ Help", callback_data="help"),
            InlineKeyboardButton("📞 Поддержка" if lang == "ru" else "📞 Support", callback_data="support")
        ],
        [
            InlineKeyboardButton("🇷🇺 Русский" if lang != "ru" else "🇬🇧 English", callback_data="lang_switch")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirm_menu(order_id, lang="ru"):
    keyboard = [
        [
            InlineKeyboardButton("✅ Подтвердить" if lang == "ru" else "✅ Confirm", callback_data=f"confirm_{order_id}"),
            InlineKeyboardButton("❌ Отклонить" if lang == "ru" else "❌ Reject", callback_data=f"reject_{order_id}")
        ],
        [
            InlineKeyboardButton("📄 Подробности" if lang == "ru" else "📄 Details", callback_data=f"details_{order_id}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_cancel_menu(order_id, lang="ru"):
    keyboard = [
        [
            InlineKeyboardButton("🚫 Отменить" if lang == "ru" else "🚫 Cancel", callback_data=f"cancel_{order_id}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)