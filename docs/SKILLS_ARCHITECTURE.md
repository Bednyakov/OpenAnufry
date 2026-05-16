# Архитектура системы навыков

## Обзор

Система навыков позволяет агенту расширять свои возможности через модульные компоненты. Каждый навык — это самодостаточный модуль с инструкциями, скриптами и справочными материалами.

## Структура директорий

```
skills/
├── __init__.py
├── loader.py                    # Загрузчик навыков
└── <skill-name>/                # Директория навыка
    ├── SKILL.md                 # Описание и инструкции (обязательно)
    ├── scripts/                 # Исполняемые скрипты (опционально)
    │   └── *.sh, *.py, etc.
    └── references/              # Справочные материалы (опционально)
        └── *.md, *.txt, etc.
```

## Формат SKILL.md

Каждый навык должен содержать файл `SKILL.md` с YAML frontmatter:

```markdown
---
name: skill-name
description: >
  Краткое описание навыка и когда его использовать.
  Может быть многострочным.
version: 1.0.0
triggers:
  - "ключевое слово 1"
  - "ключевое слово 2"
tools:
  - shell
  - read_file
requires.bins:
  - mongosh
  - docker
compatibility:
  - linux
  - darwin
---

# Полное описание навыка

Здесь идут подробные инструкции для агента...
```

### Обязательные поля:
- `name` — уникальное имя навыка
- `description` — описание для каталога навыков
- `triggers` — список ключевых слов для активации

### Опциональные поля:
- `version` — версия навыка
- `tools` — список необходимых инструментов агента
- `requires.bins` — список необходимых системных утилит
- `compatibility` — список поддерживаемых ОС

## Компоненты системы

### 1. SkillLoader (`skills/loader.py`)

Отвечает за загрузку и управление навыками:

```python
from skills.loader import SkillLoader

# Инициализация
loader = SkillLoader()
loader.scan()  # Сканирует директорию skills/

# Получение каталога для system prompt
catalog = loader.get_catalog_prompt()

# Загрузка полного навыка
skill = loader.load_full("mongo-compass")

# Поиск навыков по триггерам
matched = loader.match("найти в mongodb")
```

**Методы:**
- `scan()` — сканирует директорию и загружает метаданные
- `load_full(name)` — загружает полное содержимое навыка
- `match(query)` — находит навыки по триггерам в запросе
- `get_catalog_prompt()` — генерирует каталог для system prompt
- `get_script_path(skill_name, script_name)` — возвращает путь к скрипту

### 2. Skill Runner (`tools/skills_runner.py`)

Выполняет скрипты из навыков:

```python
from tools.skills_runner import run_skill_script

result = run_skill_script(
    skill_loader,
    "mongo-compass",
    "query_mongodb.sh",
    args=["mongodb://localhost:27017", "mydb", "users", "{}"],
    timeout=60
)
```

### 3. Интеграция в main.py

Навыки интегрированы через два инструмента:

**skill_get_info** — получает полную информацию о навыке:
```python
{
    "skill_name": "mongo-compass"
}
# Возвращает: name, description, content, triggers
```

**skill_run_script** — выполняет скрипт навыка:
```python
{
    "skill_name": "mongo-compass",
    "script_name": "query_mongodb.sh",
    "args": ["mongodb://localhost:27017", "mydb", "users", "{}"],
    "timeout": 60
}
```

## Workflow использования навыков

1. **Инициализация** (при старте агента):
   ```python
   skill_loader = SkillLoader()
   skill_loader.scan()
   ```

2. **Добавление в system prompt**:
   ```python
   SKILLS_CATALOG = skill_loader.get_catalog_prompt()
   SYSTEM_PROMPT = f"...{SKILLS_CATALOG}..."
   ```

3. **Активация навыка** (когда пользователь упоминает триггер):
   - LLM видит триггер в запросе пользователя
   - LLM вызывает `skill_get_info` для получения инструкций
   - LLM следует инструкциям из навыка
   - При необходимости вызывает `skill_run_script`

## Пример: навык mongo-compass

```
skills/mongo-compass/
├── SKILL.md                           # Инструкции по работе с MongoDB
├── scripts/
│   └── query_mongodb.sh               # Скрипт для выполнения запросов
└── references/
    └── mongodb_cheatsheet.md          # Справочник по MongoDB
```

**Триггеры:** mongo, mongodb, compass, "запрос в mongo", "найти в mongodb"

**Использование:**
1. Пользователь: "Найди все документы в mongodb коллекции users"
2. Агент видит триггер "mongodb"
3. Агент вызывает `skill_get_info("mongo-compass")`
4. Агент получает инструкции и следует им
5. Агент может вызвать `skill_run_script` или использовать `run_shell` с mongosh

## Создание нового навыка

1. Создайте директорию в `skills/`:
   ```bash
   mkdir -p skills/my-skill/{scripts,references}
   ```

2. Создайте `SKILL.md` с frontmatter и инструкциями

3. Добавьте скрипты в `scripts/` (опционально)

4. Добавьте справочные материалы в `references/` (опционально)

5. Перезапустите агента — навык загрузится автоматически

## Best Practices

1. **Триггеры:**
   - Используйте специфичные ключевые слова
   - Добавляйте синонимы и фразы
   - Избегайте слишком общих слов

2. **Инструкции:**
   - Пишите четкие пошаговые инструкции
   - Указывайте примеры использования
   - Добавляйте guardrails (правила безопасности)

3. **Скрипты:**
   - Делайте скрипты самодостаточными
   - Добавляйте проверку аргументов
   - Используйте понятные сообщения об ошибках

4. **Совместимость:**
   - Указывайте требуемые утилиты в `requires.bins`
   - Тестируйте на разных ОС
   - Добавляйте fallback-варианты

## Отладка

Проверить загрузку навыков:
```bash
python3 -c "
from skills.loader import SkillLoader
loader = SkillLoader()
loader.scan()
print(loader.get_catalog_prompt())
"
```

Проверить конкретный навык:
```bash
python3 -c "
from skills.loader import SkillLoader
loader = SkillLoader()
loader.scan()
skill = loader.load_full('mongo-compass')
print(skill.content)
"
```
