---
name: mongo-compass
description: &gt;
  Работа с MongoDB через mongosh. Используй для запросов, агрегаций,
  подсчёта документов, импорта/экспорта. Не для GUI-автоматизации Compass.
triggers:
  - mongo
  - mongodb
  - compass
  - mongosh
  - коллекция
  - документ
requires:
  bins:
    - mongosh
---

# Работа с MongoDB

## Подключение
По умолчанию: `mongodb://localhost:27017`. Если пользователь не указал URI — используй этот.

## Проверка окружения
Перед работой проверь наличие mongosh:
```bash
which mongosh
```
## Выполнение запросов
Используй run_shell с mongosh:
```bash
mongosh "<uri>" --eval "use <db>; db.<collection>.find(...).limit(50).pretty()"
```
## Workflow
1. Проверь which mongosh
2. Уточни у пользователя: URI (если не localhost), имя базы, имя коллекции
3. Сформируй JavaScript-запрос
4. Выполни через run_shell
5. Если запрос сложный — используй run_skill_script с skill_name="mongo-compass", script_name="query_mongodb.sh" и передай аргументы: URI, database, collection, query_json
## Guardrails
- Никогда не выполняй db.dropDatabase() без явного подтверждения пользователя
- Не показывай пароли в выводе
- Для больших коллекций всегда добавляй .limit(50)
- При ошибке подключения проверь, запущен ли mongod
