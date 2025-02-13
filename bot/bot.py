from datetime import datetime
from difflib import SequenceMatcher
from io import BytesIO

from django.conf import settings
from django.core.files import File
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ConversationHandler, Dispatcher, Filters, MessageHandler

from blog.models import Author, Book, Quote, Review

from .models import MessageLike

NAME, DESCRIPTION, PUBLISHED_DATE, PAGE_COUNT, IMAGE, AUTHOR_FIRST_NAME, AUTHOR_LAST_NAME = range(7)


def similar(a, b):
    """Levenshtein masofasi asosida o‘xshashlikni aniqlaydi"""
    return SequenceMatcher(None, a, b).ratio()


def start(update: Update, context: CallbackContext):
    keyboard = [[KeyboardButton("Kitob qo'shish 📚")]]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Assalomu alaykum! Kitobni qo'shishni boshlash uchun tugmani bosing.", reply_markup=reply_markup)

    return ConversationHandler.END


def handle_book_addition(update: Update, context: CallbackContext):
    update.message.reply_text("Kitob nomini kiriting:")
    return NAME


def get_name(update: Update, context: CallbackContext):
    book_name = update.message.text.strip()

    existing_books = Book.objects.all()

    for book in existing_books:
        existing_name = book.name.strip().lower()

        if similar(book_name, existing_name) > 0.85 or book_name in existing_name:
            update.message.reply_text(f"⚠️ Bunday kitob allaqachon bazada bor ({book.name})! " "Iltimos, boshqa kitob nomini kiriting.")
            return NAME

    if Book.objects.filter(name__iexact=book_name).exists():
        update.message.reply_text("⚠️ Bunday kitob allaqachon bazada bor! Iltimos, boshqa kitob nomini kiriting.")
        return NAME

    context.user_data["name"] = book_name
    update.message.reply_text("✅ Kitob nomi qabul qilindi!\n\nKitobning tavsifini kiriting:")
    return DESCRIPTION


def get_description(update: Update, context: CallbackContext):
    context.user_data["description"] = update.message.text
    update.message.reply_text("Kitobning chiqarilgan sanasini kiriting (YYYY-MM-DD formatda):")
    return PUBLISHED_DATE


def get_published_date(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    try:
        published_date = datetime.strptime(text, "%Y-%m-%d").date()
        context.user_data["published_date"] = published_date

        update.message.reply_text("✅ Sana qabul qilindi!\n\nKitobning sahifa sonini kiriting:")
        return PAGE_COUNT

    except ValueError:
        update.message.reply_text("❌ Noto‘g‘ri sana formati! Iltimos, sanani YYYY-MM-DD shaklida kiriting.")
        return PUBLISHED_DATE  # Foydalanuvchi yana kiritishi kerak bo‘ladi


def get_page_count(update: Update, context: CallbackContext):
    try:
        context.user_data["page_count"] = int(update.message.text)
    except ValueError:
        update.message.reply_text("Sahifa sonini butun son sifatida kiriting.")
        return PAGE_COUNT

    update.message.reply_text("Kitob yozuvchisining ismi:")

    return AUTHOR_FIRST_NAME


def get_author_first_name(update: Update, context: CallbackContext):
    context.user_data["author_first_name"] = update.message.text

    update.message.reply_text("Kitob yozuvchisining familiyasi:")
    return AUTHOR_LAST_NAME


def get_author_last_name(update: Update, context: CallbackContext):
    context.user_data["author_last_name"] = update.message.text

    update.message.reply_text("Kitob rasmni yuboring:")
    return IMAGE


def get_image(update: Update, context: CallbackContext):
    loading_message = update.message.reply_text("⏳ Rasm yuklanmoqda")

    file = update.message.photo[-1].get_file()
    file_content = file.download_as_bytearray()

    django_file = File(BytesIO(file_content), name="book_image.jpg")
    context.user_data["image"] = django_file

    author, created = Author.objects.get_or_create(first_name=context.user_data["author_first_name"], last_name=context.user_data["author_last_name"])

    book = Book(
        author=author,
        name=context.user_data["name"],
        description=context.user_data["description"],
        published_date=context.user_data["published_date"],
        page_count=context.user_data["page_count"],
        image=django_file,
        is_published=False,
    )

    book.save()

    loading_message.delete()

    update.message.reply_text(f"Kitob '{book.name}' muvaffaqiyatli qo'shildi!")

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Kitob qo'shish bekor qilindi.")
    return ConversationHandler.END


def send_quote(quote: Quote):
    ADMIN_IDS = settings.ADMIN_IDS

    message = (
        f"<b>📜 Yangi iqtibos qo'shildi!</b>\n\n"
        f"<b>✍️ Yozuvchi:</b> <i>{quote.writer.get_full_name()}</i>\n"
        f"<b>📚 Kitob:</b> <i>{quote.book.name if quote.book else 'Kitob ko‘rsatilmagan'}</i>\n\n"
        f"<b>📝 Iqtibos:</b>\n<blockquote>{quote.body}</blockquote>\n\n"
        f"<b>🕰 Qo‘shilgan sana:</b> {quote.created_at.strftime('%Y-%m-%d %H:%M')}"
    )

    keyboard = [
        [
            InlineKeyboardButton("O'chirish ❌", callback_data=f"delete-quote-{quote.pk}"),
            InlineKeyboardButton("Kanalga joylash ✅", callback_data=f"post-quote-{quote.pk}"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    for admin_id in ADMIN_IDS:
        bot.send_message(admin_id, message, parse_mode="HTML", reply_markup=reply_markup)


def send_review(review: Review):
    ADMIN_IDS = settings.ADMIN_IDS

    keyboard = [
        [
            InlineKeyboardButton("O'chirish ❌", callback_data=f"delete-review-{review.pk}"),
            InlineKeyboardButton("Kanalga joylash ✅", callback_data=f"post-review-{review.pk}"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📚 *Sharh Tafsilotlari* 📚\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 *Yozuvchi:* {review.writer.get_full_name()}\n"
        f"📕 *Kitob:* {review.book.name}\n"
        f"⭐️ *Bahosi:* {'⭐️' * review.rate}{'☆' * (5 - review.rate)}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💡 _{review.body}_\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🗓 *Qo‘shilgan sana:* {review.created_at.strftime('%Y-%m-%d %H:%M')}\n"
    )

    for admin_id in ADMIN_IDS:
        bot.send_message(admin_id, message, parse_mode="Markdown", reply_markup=reply_markup)


def callback_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    original_text = query.message.text

    like_button = InlineKeyboardButton("🌸 0", callback_data=f"like-{query.message.message_id}")
    keyboard = InlineKeyboardMarkup([[like_button]])

    context.bot.send_message(chat_id=settings.QUOTES_CHANNEL, text=original_text, reply_markup=keyboard)

    update.effective_message.delete()

    MessageLike.objects.create(message_id=query.message.message_id, data={"count": 0, "users": []})


def like_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    _, message_id = query.data.split("-")
    message_id = int(message_id)

    try:
        message_like = MessageLike.objects.get(message_id=message_id)

        if user_id in message_like.data["users"]:
            query.answer("Siz allaqachon like bosgansiz!", show_alert=True)

        else:
            message_like.data["count"] += 1
            message_like.data["users"].append(user_id)
            message_like.save()

            new_like_count = message_like.data["count"]
            like_button = InlineKeyboardButton(f"🌸 {new_like_count}", callback_data=f"like-{message_id}")
            keyboard = InlineKeyboardMarkup([[like_button]])

            query.edit_message_reply_markup(reply_markup=keyboard)
            query.answer("Siz muvaffaqiyatli like bosdingiz!")

    except MessageLike.DoesNotExist:
        query.answer("Xatolik yuz berdi, iltimos qayta urinib ko'ring!", show_alert=True)


def delete_handler(update: Update, context: CallbackContext):
    update.effective_message.delete()


conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(r"^Kitob qo'shish 📚$"), handle_book_addition)],
    states={
        NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
        DESCRIPTION: [MessageHandler(Filters.text & ~Filters.command, get_description)],
        PUBLISHED_DATE: [MessageHandler(Filters.text & ~Filters.command, get_published_date)],
        PAGE_COUNT: [MessageHandler(Filters.text & ~Filters.command, get_page_count)],
        AUTHOR_FIRST_NAME: [MessageHandler(Filters.text & ~Filters.command, get_author_first_name)],
        AUTHOR_LAST_NAME: [MessageHandler(Filters.text & ~Filters.command, get_author_last_name)],
        IMAGE: [MessageHandler(Filters.photo & ~Filters.command, get_image)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)


bot = Bot(token=settings.BOT_TOKEN)


dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(conversation_handler)
dispatcher.add_handler(CallbackQueryHandler(callback_handler, pattern="post-"))
dispatcher.add_handler(CallbackQueryHandler(like_handler, pattern="like-"))
dispatcher.add_handler(CallbackQueryHandler(delete_handler, pattern="delete-"))
