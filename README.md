# Ads-Online Backend

## Описание проекта

Ads-Online - это платформа для публикации объявлений. Данный репозиторий содержит backend часть проекта, который взаимодействует с фронтенд-частью (не включена в этот репозиторий).

### Основные возможности

- **Аутентификация и авторизация пользователей**: Поддержка регистрации, входа, восстановления пароля через электронную почту.
- **Управление ролями пользователей**: Разделение прав доступа между обычными пользователями и администраторами.
- **Управление объявлениями**: Пользователи могут создавать, просматривать, редактировать и удалять свои объявления. 
    Администраторы могут управлять всеми объявлениями на платформе.
- **Комментарии к объявлениям**: Пользователи могут оставлять отзывы на объявления.
- **Поиск по объявлениям**: Фильтрация объявлений по ключевым словам.

## Технологический стек

- **Django & Django REST Framework (DRF)**: Основа backend-сервера. DRF используется для создания RESTful API.
- **Djoser**: Библиотека для управления аутентификацией и регистрацией пользователей.
- **PostgreSQL**: Система управления базами данных.
- **Django ORM**: Работа с базой данных через объектно-ориентированный подход.
- **Serializers & ViewSets**: Компоненты DRF для обработки данных и логики представления.
- **Filter**: Фильтрация данных в API.
- **CORS (Cross-Origin Resource Sharing)**: Настройка политик CORS для безопасного взаимодействия с фронтенд-частью.
- **Docker & Docker Compose**: Контейнеризация приложения и управление многоконтейнерными приложениями.
- **Swagger & ReDoc**: Автоматическая документация API с возможностями интерактивного тестирования.
- **Git**: Система контроля версий для управления кодом проекта.
- **PEP8**: Соблюдение стандартов стиля кода для Python.
- **GitHub Actions/CI**: Интеграция для автоматизации тестирования и развертывания.

## Как начать использовать

### Предварительные требования

- Docker
- Docker Compose

### Запуск проекта

1. **Клонирование репозитория**

   git clone https://github.com/YGilm/ads-online.git
   cd ads-online

2. Настройка переменных окруженияСоздайте файл .env на основе .env.example, указав необходимые параметры. 
3. Запуск контейнеров
   
   docker-compose up --build

После сборки и запуска контейнеров, backend будет доступен по адресу http://localhost:8000.

**Документация API**

После запуска проекта, документация API будет доступна по адресам:

Swagger UI: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/
