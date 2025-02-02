import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse


class Command(BaseCommand):
    help = "Serverga webhook'ni sozlash uchun"

    def add_arguments(self, parser):
        parser.add_argument("baseurl", nargs=1, type=str)

    def handle(self, *args, **options):
        baseurl = options["baseurl"][0]

        webhook_url = baseurl + reverse("telegram_webhook")

        print(webhook_url)

        url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/setWebhook"

        data = {"url": webhook_url}
        response = requests.post(url, data=data)

        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS(f"Webhook muvaffaqiyatli o'rnatildi: {webhook_url}"))
        else:
            self.stdout.write(self.style.ERROR(f"Webhookni o'rnatishda xatolik yuz berdi: {response.text}"))
