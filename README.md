# Telegram Bot For A Freelancer Portfolio

## English

This is a simple Telegram bot built for a freelancer portfolio. It shows how a small business can automate first contact with clients, answer common questions, and collect service requests directly inside Telegram.

The bot is suitable for freelancers, agencies, consultants, local services, online stores, and small businesses that want a fast and affordable Telegram assistant.

### What The Bot Does

- Greets new users with a short introduction
- Shows a help menu with available commands
- Answers frequently asked questions by keywords
- Collects client requests through a simple order form
- Saves each request with date, time, name, phone number, Telegram ID, and username
- Politely guides users when it does not understand a message

### Main Commands

```text
/start
/help
/order
/cancel
```

### FAQ Keywords

```text
price
hours
address
delivery
```

The FAQ is stored as a simple dictionary in the code, so it can be quickly changed for any niche or business.

### Example User Flow

```text
User: /start
Bot: Hello! I am a freelancer portfolio bot.

User: What is the price?
Bot: The price depends on the project...

User: /order
Bot: Let's create your request. What is your name?

User: John Smith
Bot: Thank you! Now please send your phone number.

User: +1 555 123 4567
Bot: Thank you! Your request has been saved.
```

### Business Value

This bot helps a business respond to clients faster without manually answering the same questions again and again.

It can be used as:

- A lead collection bot
- A portfolio assistant
- A service request bot
- A FAQ bot for a small business
- A basic client intake form

### What Can Be Customized

- Greeting text
- Help message
- FAQ keywords and answers
- Order form questions
- Saved request format
- Business name and tone of voice
- Deployment setup for 24/7 hosting

### Technologies Used

- Python
- python-telegram-bot
- Async handlers
- Environment variables for secure token storage
- Text file storage for simple client requests

### Security

The Telegram bot token is not stored directly in the code. It is loaded from an environment variable named `BOT_TOKEN`.

Private files such as `.env`, `orders.txt`, and `.venv` should not be uploaded to GitHub.

### Project Goal

The goal of this project is to demonstrate a practical Telegram automation that can be adapted for real client work. It is intentionally simple, readable, and easy to modify for different businesses.

---

## Русский

Это простой Telegram-бот для портфолио фрилансера. Он показывает, как малый бизнес может автоматизировать первое общение с клиентами, отвечать на частые вопросы и принимать заявки прямо в Telegram.

Бот подойдет фрилансерам, агентствам, консультантам, локальным сервисам, интернет-магазинам и небольшим компаниям, которым нужен быстрый и доступный Telegram-ассистент.

### Что Умеет Бот

- Приветствует новых пользователей
- Показывает меню помощи с доступными командами
- Отвечает на частые вопросы по ключевым словам
- Принимает заявки через простую форму
- Сохраняет каждую заявку с датой, временем, именем, телефоном, Telegram ID и username
- Вежливо подсказывает, что делать, если не понял сообщение

### Основные Команды

```text
/start
/help
/order
/cancel
```

### Ключевые Слова FAQ

```text
price
hours
address
delivery
```

FAQ хранится в коде как простой словарь, поэтому его легко изменить под любую нишу или бизнес.

### Пример Диалога

```text
User: /start
Bot: Hello! I am a freelancer portfolio bot.

User: What is the price?
Bot: The price depends on the project...

User: /order
Bot: Let's create your request. What is your name?

User: John Smith
Bot: Thank you! Now please send your phone number.

User: +1 555 123 4567
Bot: Thank you! Your request has been saved.
```

### Польза Для Бизнеса

Бот помогает бизнесу быстрее отвечать клиентам и не тратить время на одни и те же повторяющиеся вопросы.

Его можно использовать как:

- Бота для сбора заявок
- Ассистента для портфолио
- Бота для приема обращений
- FAQ-бота для малого бизнеса
- Простую форму первичного контакта с клиентом

### Что Можно Настроить

- Приветствие
- Сообщение помощи
- Ключевые слова и ответы FAQ
- Вопросы формы заявки
- Формат сохранения заявки
- Название бизнеса и стиль общения
- Деплой на хостинг для работы 24/7

### Использованные Технологии

- Python
- python-telegram-bot
- Асинхронные обработчики
- Переменные окружения для безопасного хранения токена
- Сохранение заявок в текстовый файл

### Безопасность

Токен Telegram-бота не хранится прямо в коде. Он загружается из переменной окружения `BOT_TOKEN`.

Файлы `.env`, `orders.txt` и `.venv` нельзя загружать на GitHub.

### Цель Проекта

Цель проекта - показать практичную Telegram-автоматизацию, которую можно адаптировать под реальные задачи клиентов. Бот специально сделан простым, понятным и удобным для изменения под разные бизнесы.
