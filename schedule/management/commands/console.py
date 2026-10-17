from django.core.management.base import BaseCommand

from schedule.console import run


class Command(BaseCommand):
    help = "Запуск консольного інтерфейсу керування шкільним розкладом"

    def handle(self, *args, **options):
        run()