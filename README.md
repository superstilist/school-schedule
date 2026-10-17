# School Schedule Management System (Система керування шкільним розкладом)

Django project for managing school subjects, teachers, classes and students.

## Models

- **Subject** (Предмет) — school subject.
- **Teacher** (Вчитель) — teacher linked to a subject via `ForeignKey`.
- **Class** (Клас) — school class.
- **Student** (Учень) — student linked to a class via `ForeignKey`.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
