# Backend of Marketplace, DRF

Онлайн-маркетплейс для продажи/покупки одежды(бекенд часть).

## Содержание

-[Технологии](#технологии)
-[Установка](#установка)
-[Api](#api)

## Технологии
- Python 3.12.3
- Django 5.1
- Django REST Framework 3.15.2
- PostgreSQL

## Установка

### Предварительные требования
1. **Python**: Установить Python версии указанной в "Технологиях"
2. **Poetry**: Установить Poetry версии указанной в "Технологиях"

### Шаги установки проекта
1. **Клонировать репозиторий проекта**
2. **Установите зависимости проекта**:
    ```bash
    poetry install
    ```
3. **Создайте виртуальное окружение**: 
    - Poetry автоматически создает виртуальное окружение. Чтобы активировать его, выполните:
    ```bash
    poetry shell
    ```
4. **Настройка базы данных (если необходимо)**:
   - Подключите свою бд в core/settings.py, Выполните миграции базы данных, создайте суперюзера для доступа к админке:
     ```bash
      python manage.py migrate
      python manage.py createsuperuser
     ```
5. **Запуск проекта**:
   - Запустите проект с помощью команды:
     ```bash
      python manage.py runserver
     ```

## Api
В этом разделе приведены инструкции по использованию API вашего проекта.

### Аутентификация
Для доступа к защищенным эндпоинтам необходимо использовать токен аутентификации. Токен передается в заголовке `Authorization` в следующем формате: Authorization: Bearer <your-token-here>

### Эндпоинты для Users
#### 1. Регистрация
```bash
URL: /api/v1/users/registration/
Method: POST
```
#### 2. Получение токена
```bash
URL: /api/v1/users/token/
Method: POST
Fields: email, password
```
#### 3. Обновление токена
```bash
URL: /api/v1/users/token/refresh/
Method: POST
Fields: refresh
```
Каждые 30 минут(можно настроить в core/settings.py)

### Эндпоинты для Products
#### 1. Список всех продуктов
```bash
URL: /api/v1/products/products/
Method: GET
```
#### 2. Информация о конкретном продукте
```bash
URL: /api/v1/products/products/{id}/
Method: GET
```
#### 3. Создание нового продукта пользователем
```bash
URL: /api/v1/products/seller/products/
Method: POST
Headers: Authorization: Bearer <your-token-here>
```
#### 4. Отправка на модерацию
```bash
URL: /api/v1/products/seller/products/{id}/send_on_moderation/
Method: POST
Headers: Authorization: Bearer <your-token-here>
```
#### 5. Публикация после ревью модерации
Срабатывает только если модератор поставил статус "Одобрено" в админ панеле
```bash
URL: /api/v1/products/seller/products/{id}/publish/
Method: POST
Headers: Authorization: Bearer <your-token-here>
```
#### 6. Список всех категорий
```bash
URL: /api/v1/products/categories/
Method: GET
```
Категории у которых поле Parent не равно null являются ПОДКАТЕГОРИЯМИ 
#### 7. Информация о конкретной категории
```bash
URL: /api/v1/products/categories/{id}/
Method: GET
```
#### 8. Список всех стилей
```bash
URL: /api/v1/products/styles/
Method: GET
```
#### 9. Информация о конкретном стиле
```bash
URL: /api/v1/products/styles/{id}/
Method: GET
```










