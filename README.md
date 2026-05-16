# OpenAnufry
Российский агент Ануфрий на Python с долговременной памятью

```
agent-Anufry/
├── main.py              # Gateway + Agent Loop
├── tools/
│   ├── shell.py         # Выполнение команд
│   ├── filesystem.py    # Работа с файлами
│   ├── browser.py       # Управление браузером через CDP
│   └── memory_tools.py  # Инструменты памяти
├── memory/
│   ├── manager.py       # Менеджер долговременной памяти
│   ├── agent_memory.db  # SQLite база данных
│   └── README.md        # Документация памяти
├── config.py            # Конфигурация
└── requirements.txt
```

## ✨ Новое: Система долговременной памяти

Агент теперь имеет **долговременную память**:
- 🧠 Автоматически сохраняет важные диалоги и факты
- 🔍 Семантический поиск через OpenAI embeddings
- 🎯 Автоматическая классификация важности информации
- 🧹 Умная очистка устаревших данных
- 💾 Персистентность между сессиями

**Быстрый старт:** см. [MEMORY_QUICKSTART.md](MEMORY_QUICKSTART.md)


# Запуск

## 1. Установка зависимостей
pip install -r requirements.txt

playwright install chromium

## 2. Настройка API-ключа
export OPENAI_API_KEY="sk-..."

## 3. Запуск
python main.py


# Пример работы

```
==================================================
🤖 Агент с доступом к shell (Ctrl+C для выхода)
==================================================

💬 Вы: Покажи содержимое текущей директории

⏳ Агент думает...

--- Итерация 1 ---
🔧 Вызов: list_dir({"path": "."})
📤 Результат: {"success": true, "items": [...]}

🤖 Агент: В рабочей директории находятся следующие файлы: ...

💬 Вы: Установи mongosh и проверь подключение к localhost:27017

⏳ Агент думает...

--- Итерация 1 ---
🔧 Вызов: run_shell({"command": "which mongosh || sudo apt install -y mongodb-mongosh"})
📤 Результат: {"success": true, "stdout": "/usr/bin/mongosh", ...}

--- Итерация 2 ---
🔧 Вызов: run_shell({"command": "mongosh \"mongodb://localhost:27017\" --eval \"db.adminCommand('ping')\""})
📤 Результат: {"success": true, "stdout": "{ ok: 1 }", ...}

🤖 Агент: MongoDB Shell установлен. Подключение к localhost:27017 успешно — сервер отвечает { ok: 1 }.
```
