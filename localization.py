# localization.py
from telegram import Update

class Localization:
    MESSAGES = {
        "ru": {
            "welcome": "✨ <b>Добро пожаловать в StarShop!</b> ✨\nВыберите количество звезд для покупки:\n🌟 Сияйте ярче с нашими звездами! 🌟",
            "order_created": "🌟 <b>Заявка #{order_id} создана!</b>\nКоличество звезд: {stars}\nСтатус: ⏳ Ожидает подтверждения\nВы можете отменить заявку или проверить статус:",
            "order_confirmed": "🎉 <b>Заявка #{order_id} подтверждена!</b>\nВы приобрели {stars} звезд! 🌟",
            "order_rejected": "😔 <b>Заявка #{order_id} отклонена.</b>\nПопробуйте снова или свяжитесь с поддержкой: @SupportStarShop",
            "order_cancelled": "🚫 <b>Заявка #{order_id} отменена.</b>",
            "order_not_found": "⚠️ Заявка не найдена.",
            "no_orders": "📭 У вас нет активных заявок.",
            "status": "📋 <b>Ваши заявки:</b>\n{orders}",
            "history": "📜 <b>История покупок:</b>\n{history}",
            "help": "❓ <b>Инструкция по StarShop</b> ❓\n1. Выберите количество звезд для покупки.\n2. Дождитесь подтверждения от администратора.\n3. Проверяйте статус заявок через 'Мои заявки'.\n4. Отменяйте заявки, если они не обработаны.\n5. Просматривайте историю покупок.\n📩 По вопросам: @SupportStarShop",
            "admin_new_order": "📬 <b>Новая заявка #{order_id}</b>\nПользователь: @{username}\nЗвезды: {stars}\nВремя: {timestamp}",
            "admin_order_cancelled": "🚫 Заявка #{order_id} от @{username} была отменена.",
            "order_details": "📄 <b>Подробности заявки #{order_id}</b>\nПользователь: @{username}\nЗвезды: {stars}\nСтатус: {status}\nВремя: {timestamp}",
            "no_permission": "⚠️ Вы не можете отменить чужую заявку.",
            "support": "📞 <b>Поддержка</b>\nСвяжитесь с нами: @SupportStarShop"
        },
        "en": {
            "welcome": "✨ <b>Welcome to StarShop!</b> ✨\nChoose the number of stars to purchase:\n🌟 Shine brighter with our stars! 🌟",
            "order_created": "🌟 <b>Order #{order_id} created!</b>\nStars: {stars}\nStatus: ⏳ Pending\nYou can cancel the order or check its status:",
            "order_confirmed": "🎉 <b>Order #{order_id} confirmed!</b>\nYou purchased {stars} stars! 🌟",
            "order_rejected": "😔 <b>Order #{order_id} rejected.</b>\nTry again or contact support: @SupportStarShop",
            "order_cancelled": "🚫 <b>Order #{order_id} cancelled.</b>",
            "order_not_found": "⚠️ Order not found.",
            "no_orders": "📭 You have no active orders.",
            "status": "📋 <b>Your orders:</b>\n{orders}",
            "history": "📜 <b>Purchase history:</b>\n{history}",
            "help": "❓ <b>StarShop Guide</b> ❓\n1. Choose the number of stars to buy.\n2. Wait for admin approval.\n3. Check order status via 'My Orders'.\n4. Cancel orders if not processed.\n5. View your purchase history.\n📩 Contact us: @SupportStarShop",
            "admin_new_order": "📬 <b>New order #{order_id}</b>\nUser: @{username}\nStars: {stars}\nTime: {timestamp}",
            "admin_order_cancelled": "🚫 Order #{order_id} by @{username} was cancelled.",
            "order_details": "📄 <b>Order #{order_id} details</b>\nUser: @{username}\nStars: {stars}\nStatus: {status}\nTime: {timestamp}",
            "no_permission": "⚠️ You cannot cancel someone else's order.",
            "support": "📞 <b>Support</b>\nContact us: @SupportStarShop"
        }
    }

    @staticmethod
    def get_message(update: Update, key: str, lang: str = "ru", **kwargs):
        return Localization.MESSAGES.get(lang, Localization.MESSAGES["ru"]).get(key, "").format(**kwargs)