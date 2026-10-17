# Система керування шкільним розкладом

Django-проєкт для управління предметами, вчителями, класами, учнями, розкладом занять та оцінками.

## Моделі

- `Subject` (Предмет) — назва, опис
- `Teacher` (Вчитель) — ім'я, прізвище, предмет (ForeignKey → Subject)
- `Class` (Клас) — назва, рік навчання
- `Student` (Учень) — ім'я, прізвище, клас (ForeignKey → Class)
- `Schedule` (Розклад) — день тижня, година початку, предмет, клас, вчитель (ForeignKey)
- `Grade` (Оцінка) — учень, предмет, оцінка, дата (ForeignKey)

## Встановлення

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

## Запуск консольного інтерфейсу

```bash
python console.py
# або
python manage.py console
```

## Тести

```bash
python manage.py test
```

## Адмін-панель

```bash
python manage.py createsuperuser
python manage.py runserver
```

Відкрийте http://127.0.0.1:8000/admin/