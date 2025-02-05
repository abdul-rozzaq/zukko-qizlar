from datetime import datetime
from difflib import SequenceMatcher
from io import BytesIO

from django.conf import settings
from django.core.files import File
from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, Dispatcher, Filters, MessageHandler

from blog.models import Author, Book

# States for the conversation
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
