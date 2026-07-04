BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

CATEGORIES = {
    "Ключи активации": "activation_keys",
    "Гайды": "guides",
    "Подписки": "subscriptions",
}

PRODUCTS = {
    "activation_keys": [
        {"id": 1, "name": "Windows 11 Pro", "price": 1500, "description": "Лицензионный ключ Windows 11 Pro. Бессрочная активация."},
        {"id": 2, "name": "Office 2024 Pro", "price": 2500, "description": "Ключ активации Microsoft Office 2024 Professional."},
    ],
    "guides": [
        {"id": 3, "name": "Гайд по Python", "price": 500, "description": "PDF-гайд для начинающих Python-разработчиков (150 стр.)."},
        {"id": 4, "name": "Гайд по Telegram Bot API", "price": 700, "description": "Полный гайд по созданию ботов на aiogram 3.x."},
    ],
    "subscriptions": [
        {"id": 5, "name": "VPN на месяц", "price": 300, "description": "Доступ к VPN-серверу на 30 дней."},
        {"id": 6, "name": "VPN на год", "price": 2500, "description": "Доступ к VPN-серверу на 365 дней."},
    ],
}

KEYS_POOL = {
    1: ["WIN11-AAAA-BBBB-CCCC", "WIN11-DDDD-EEEE-FFFF"],
    2: ["OFF24-1111-2222-3333", "OFF24-4444-5555-6666"],
    3: [],  # гайды — файлы
    4: [],
    5: ["VPN-USER-001:pass123", "VPN-USER-002:pass456"],
    6: ["VPN-YEAR-001:pass789"],
}
