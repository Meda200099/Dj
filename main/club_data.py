CLUB = {
    "club_name": "Nexus Arena",
    "slogan": "Играй на максимуме — без компромиссов",
    "quality_text": "43 игровых места, мощные ПК, низкий пинг, комфортные кресла и атмосфера для побед.",
    "phone": "+7 (495) 777-00-99",
    "email": "play@nexus-arena.ru",
    "address": "г. Москва, ул. Геймерская, д. 42",
    "work_hours": "Ежедневно: 10:00–02:00",
    "metro": "м. Технопарк, 5 мин пешком",
    "social_vk": "https://vk.com/nexusarena",
    "social_tg": "https://t.me/nexusarena",
}

BOOKING_BUTTONS = [
    {"icon": "🎮", "title": "Стандарт", "anchor": "booking"},
    {"icon": "⚡", "title": "Pro", "anchor": "booking"},
    {"icon": "👑", "title": "VIP-зона", "anchor": "booking"},
    {"icon": "🏆", "title": "Bootcamp", "anchor": "booking"},
    {"icon": "🌙", "title": "Ночной пакет", "anchor": "booking"},
]

TARIFFS = [
    {
        "slug": "standart",
        "icon": "🎮",
        "title": "Стандарт",
        "text": "1080p, RTX 4060, 144 Гц — для комфортной игры.",
        "lead": "Оптимальный тариф для повседневных сессий и казуальных игр.",
        "blocks": [
            {
                "title": "Что входит",
                "items": [
                    "Intel i5-13400F / Ryzen 5 5600, 16 ГБ DDR5",
                    "GeForce RTX 4060, монитор 24\" 144 Гц IPS",
                    "HyperX Alloy Origins, Logitech G Pro X Superlight",
                    "SteelSeries Arctis 7 — наушники с микрофоном",
                ],
            },
            {
                "title": "Подходит для",
                "items": [
                    "CS2, Dota 2, Valorant",
                    "GTA V, Fortnite, Apex Legends",
                    "Стримы и общение с друзьями",
                ],
            },
        ],
        "duration": "от 1 часа",
        "price": "150 ₽/час",
    },
    {
        "slug": "pro",
        "icon": "⚡",
        "title": "Pro",
        "text": "2K, RTX 4070 Super, 240 Гц — для соревновательного гейминга.",
        "lead": "Максимальный FPS и отклик для ranked и турниров.",
        "blocks": [
            {
                "title": "Характеристики",
                "items": [
                    "Intel i7-14700F / Ryzen 7 7800X3D, 32 ГБ DDR5",
                    "GeForce RTX 4070 Super, монитор 27\" 240 Гц",
                    "Wooting 60HE, Finalmouse Starlight",
                    "Стабильный пинг до 5 мс",
                ],
            },
            {
                "title": "Для кого",
                "items": [
                    "Ранкед в CS2 и Valorant",
                    "Тренировки команд",
                    "Стримеры и контент-мейкеры",
                ],
            },
        ],
        "duration": "от 1 часа",
        "price": "250 ₽/час",
    },
    {
        "slug": "vip",
        "icon": "👑",
        "title": "VIP",
        "text": "Отдельная комната, RTX 5090, 4K — полная приватность.",
        "lead": "Закрытая зона с премиальным железом и сервисом.",
        "blocks": [
            {
                "title": "Преимущества",
                "items": [
                    "Intel i9-14900KS / Ryzen 9 9950X, 64 ГБ DDR5",
                    "GeForce RTX 5090, OLED 32\" 4K 240 Гц",
                    "Отдельная комната на 1–4 человека",
                    "Мини-бар и заказ еды в зал",
                ],
            },
            {
                "title": "Идеально для",
                "items": [
                    "Командных тренировок",
                    "Стрим-сессий и записи",
                    "Приватных вечеринок",
                ],
            },
        ],
        "duration": "от 2 часов",
        "price": "450 ₽/час",
    },
    {
        "slug": "bootcamp",
        "icon": "🏆",
        "title": "Bootcamp",
        "text": "5 мест в одной комнате — командный тариф со скидкой.",
        "lead": "Аренда bootcamp-зала для команды на 5 игроков.",
        "blocks": [
            {
                "title": "Включено",
                "items": [
                    "5 Pro-мест в изолированной комнате",
                    "Общий экран 75\" для разбора демо",
                    "Белая доска и таймер",
                    "Скидка 20% при брони от 3 часов",
                ],
            },
            {
                "title": "Для команд",
                "items": [
                    "Подготовка к турнирам",
                    "Совместные тренировки",
                    "Корпоративные ивенты",
                ],
            },
        ],
        "duration": "от 3 часов",
        "price": "1 000 ₽/час (вся комната)",
    },
    {
        "slug": "nochnoy",
        "icon": "🌙",
        "title": "Ночной пакет",
        "text": "Безлимит с 23:00 до 06:00 — выгодно для ночных сессий.",
        "lead": "Фиксированная цена за всю ночь на месте Стандарт или Pro.",
        "blocks": [
            {
                "title": "Условия",
                "items": [
                    "Действует с 23:00 до 06:00",
                    "Стандарт — 600 ₽, Pro — 900 ₽",
                    "Напиток в подарок",
                    "Бронь только до 22:30",
                ],
            },
            {
                "title": "Важно",
                "items": [
                    "Одно место на весь период",
                    "Продление по обычному тарифу",
                    "VIP и Bootcamp — по отдельным условиям",
                ],
            },
        ],
        "duration": "8 часов",
        "price": "от 600 ₽",
    },
    {
        "slug": "paket-3ch",
        "icon": "📦",
        "title": "Пакет 3 часа",
        "text": "Три часа игры со скидкой 10% на любой тариф.",
        "lead": "Выгодный пакет для длинной игровой сессии.",
        "blocks": [
            {
                "title": "Выгода",
                "items": [
                    "Скидка 10% от почасовой ставки",
                    "Можно комбинировать с акциями",
                    "Доступно на Стандарт и Pro",
                ],
            },
            {
                "title": "Как воспользоваться",
                "items": [
                    "Выберите тариф при бронировании",
                    "Укажите время начала и место",
                    "Оплата на ресепшене при посадке",
                ],
            },
        ],
        "duration": "3 часа",
        "price": "от 405 ₽",
    },
]

PRICES = [
    {"icon": "🎮", "name": "Стандарт", "price": "150 ₽/час"},
    {"icon": "⚡", "name": "Pro", "price": "250 ₽/час"},
    {"icon": "👑", "name": "VIP", "price": "450 ₽/час"},
    {"icon": "🏆", "name": "Bootcamp (5 мест)", "price": "1 000 ₽/час"},
    {"icon": "🌙", "name": "Ночной пакет", "price": "от 600 ₽"},
    {"icon": "📦", "name": "Пакет 3 часа", "price": "−10%"},
]

STANDARD_SPECS = {
    "cpu": "Intel i5-13400F",
    "gpu": "RTX 4060 8 ГБ",
    "ram": "16 ГБ DDR5",
    "monitor": "24\" 144 Гц IPS",
    "storage": "1 ТБ NVMe SSD",
}

PRO_SPECS = {
    "cpu": "Ryzen 7 7800X3D",
    "gpu": "RTX 4070 Super 12 ГБ",
    "ram": "32 ГБ DDR5",
    "monitor": "27\" 240 Гц IPS",
    "storage": "2 ТБ NVMe SSD",
}

VIP_SPECS = {
    "cpu": "Intel i9-14900KS",
    "gpu": "RTX 5090 32 ГБ",
    "ram": "64 ГБ DDR5",
    "monitor": "32\" OLED 4K 240 Гц",
    "storage": "4 ТБ NVMe SSD",
}

BOOTCAMP_SPECS = PRO_SPECS.copy()


def _build_standard_seats():
    seats = []
    rows = [
        (1, 8),
        (2, 8),
        (3, 8),
    ]
    num = 1
    for row, count in rows:
        for _ in range(count):
            value = f"S-{num:02d}"
            seats.append({
                "value": value,
                "label": f"{value} — Стандарт, ряд {row}",
                "zone": "standard",
                "row": row,
            })
            num += 1
    return seats


def _build_pro_seats():
    seats = []
    rows = [
        (1, 6),
        (2, 6),
    ]
    num = 1
    for row, count in rows:
        for _ in range(count):
            value = f"P-{num:02d}"
            seats.append({
                "value": value,
                "label": f"{value} — Pro, ряд {row}",
                "zone": "pro",
                "row": row,
            })
            num += 1
    return seats


def _build_vip_seats():
    return [
        {"value": "V-01", "label": "V-01 — VIP комната «Neon»", "zone": "vip", "row": 1},
        {"value": "V-02", "label": "V-02 — VIP комната «Pulse»", "zone": "vip", "row": 1},
    ]


def _build_bootcamp_seats():
    return [
        {
            "value": f"B-{num:02d}",
            "label": f"B-{num:02d} — Bootcamp (место {num})",
            "zone": "bootcamp",
            "row": 1,
        }
        for num in range(1, 6)
    ]


SEATS = (
    _build_standard_seats()
    + _build_pro_seats()
    + _build_vip_seats()
    + _build_bootcamp_seats()
)


def _computer_from_seat(seat, specs, zone_name, tariff):
    return {
        "id": seat["value"],
        "zone": zone_name,
        "zone_key": seat["zone"],
        "tariff": tariff,
        "row": seat["row"],
        "label": seat["label"],
        **specs,
    }


COMPUTERS = [
    *[
        _computer_from_seat(s, STANDARD_SPECS, "Зал Стандарт", "Стандарт")
        for s in _build_standard_seats()
    ],
    *[
        _computer_from_seat(s, PRO_SPECS, "Зал Pro", "Pro")
        for s in _build_pro_seats()
    ],
    *[
        _computer_from_seat(s, VIP_SPECS, "VIP-комнаты", "VIP")
        for s in _build_vip_seats()
    ],
    *[
        _computer_from_seat(s, BOOTCAMP_SPECS, "Bootcamp", "Pro")
        for s in _build_bootcamp_seats()
    ],
]

ZONE_FILTERS = [
    {"key": "all", "label": "Все зоны", "icon": "🖥️"},
    {"key": "standard", "label": "Стандарт", "icon": "🎮"},
    {"key": "pro", "label": "Pro", "icon": "⚡"},
    {"key": "vip", "label": "VIP", "icon": "👑"},
    {"key": "bootcamp", "label": "Bootcamp", "icon": "🏆"},
]

ZONES = [
    {
        "icon": "🎮",
        "name": "Зал Стандарт",
        "key": "standard",
        "seats_count": 24,
        "text": "24 места в открытой зоне с общим экраном трансляций и турниров.",
        "features": ["RTX 4060", "144 Гц", "DXRacer кресла", "Стрим-зона"],
    },
    {
        "icon": "⚡",
        "name": "Зал Pro",
        "key": "pro",
        "seats_count": 12,
        "text": "12 мест с 240 Гц мониторами для соревновательного гейминга.",
        "features": ["RTX 4070 Super", "240 Гц", "Wooting клавиатуры", "Anti-ghosting сеть"],
    },
    {
        "icon": "👑",
        "name": "VIP-комнаты",
        "key": "vip",
        "seats_count": 2,
        "text": "2 приватные комнаты с премиальным железом и мини-баром.",
        "features": ["RTX 5090", "OLED 4K", "Приватность", "Заказ еды"],
    },
    {
        "icon": "🏆",
        "name": "Bootcamp",
        "key": "bootcamp",
        "seats_count": 5,
        "text": "Командная комната на 5 игроков с экраном 75\" для разбора демо.",
        "features": ["5 Pro-мест", "Demo-экран", "Таймер", "Командная скидка"],
    },
]

PERIPHERALS = [
    {"icon": "⌨️", "name": "HyperX Alloy Origins", "text": "Механические клавиатуры на местах Стандарт."},
    {"icon": "⌨️", "name": "Wooting 60HE", "text": "Hall-effect клавиатуры в зоне Pro и Bootcamp."},
    {"icon": "🖱️", "name": "Logitech G Pro X Superlight", "text": "Лёгкие беспроводные мыши с настраиваемым DPI."},
    {"icon": "🎧", "name": "SteelSeries Arctis 7", "text": "Наушники с шумоподавлением на всех местах."},
    {"icon": "🪑", "name": "DXRacer Master", "text": "Эргономичные кресла для длинных сессий."},
    {"icon": "🖥️", "name": "BenQ / Samsung Odyssey", "text": "IPS и OLED мониторы с низким input lag."},
]

FAQ = [
    {
        "q": "Как забронировать место?",
        "a": "Зарегистрируйтесь на сайте, выберите тариф, дату, время и свободное место в форме бронирования.",
    },
    {
        "q": "Можно ли отменить бронь?",
        "a": "Да, свяжитесь с администратором или отмените заявку в личном кабинете до начала сессии.",
    },
    {
        "q": "Есть ли скидки для команд?",
        "a": "Bootcamp-зал со скидкой 20% при брони от 3 часов. Также действует пакет «3 часа» со скидкой 10%.",
    },
    {
        "q": "Нужна ли своя периферия?",
        "a": "Нет, на каждом месте полный комплект. Можно принести свою мышь или коврик.",
    },
]


def get_tariff(slug):
    for tariff in TARIFFS:
        if tariff["slug"] == slug:
            return tariff
    return None


def get_computers_by_zone(zone_key):
    if not zone_key or zone_key == "all":
        return COMPUTERS
    return [pc for pc in COMPUTERS if pc["zone_key"] == zone_key]


def get_seats_for_tariff(tariff_title):
    mapping = {
        "Стандарт": "standard",
        "Pro": "pro",
        "VIP": "vip",
        "Bootcamp": "bootcamp",
        "Ночной пакет": None,
        "Пакет 3 часа": None,
    }
    zone = mapping.get(tariff_title)
    if zone is None and tariff_title in ("Ночной пакет", "Пакет 3 часа"):
        return [s for s in SEATS if s["zone"] in ("standard", "pro")]
    if zone:
        return [s for s in SEATS if s["zone"] == zone]
    return SEATS
