import json
from io import BytesIO

import requests
from django.conf import settings
from django.core.files import File
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher, Filters, MessageHandler

from .bot import bot, dispatcher


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":

        payload = json.loads(request.body)
        update = Update.de_json(payload, bot)

        dispatcher.process_update(update)

        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
