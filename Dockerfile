# Используем официальный образ Python как базовый
FROM python:3.10-slim

# Устанавливаем рабочий каталог в контейнере
WORKDIR /app

# Копируем файл зависимостей в рабочий каталог
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код проекта в рабочий каталог
COPY . .

# Задаём переменные окружения
ENV DJANGO_SETTINGS_MODULE 'config.settings'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
