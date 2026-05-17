# 🏠 Руководство по работе с локальными LLM

Агент Ануфрий поддерживает работу с локальными LLM через OpenAI-совместимый API. Это позволяет использовать модели на вашем компьютере без отправки данных в облако.

## 📋 Содержание

- [Поддерживаемые провайдеры](#поддерживаемые-провайдеры)
- [Быстрый старт](#быстрый-старт)
- [Настройка провайдеров](#настройка-провайдеров)
- [Примеры конфигураций](#примеры-конфигураций)
- [Troubleshooting](#troubleshooting)

---

## 🔌 Поддерживаемые провайдеры

| Провайдер | Описание | Function Calling | Установка |
|-----------|----------|------------------|-----------|
| **OpenAI** | Официальный API OpenAI | ✅ | Не требуется |
| **OpenRouter** | Агрегатор LLM API | ✅ | Не требуется |
| **Ollama** | Локальный запуск моделей | ✅ | [ollama.com](https://ollama.com) |
| **LM Studio** | GUI для локальных моделей | ✅ | [lmstudio.ai](https://lmstudio.ai) |
| **LocalAI** | Self-hosted OpenAI API | ✅ | [localai.io](https://localai.io) |
| **vLLM** | Высокопроизводительный inference | ✅ | [vllm.ai](https://vllm.ai) |
| **Text Gen WebUI** | Oobabooga WebUI | ⚠️ | [GitHub](https://github.com/oobabooga/text-generation-webui) |

---

## 🚀 Быстрый старт

### 1. Установка Ollama (рекомендуется для начинающих)

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Запуск модели
ollama pull llama3.2
ollama serve
```

### 2. Настройка .env файла

```bash
# Для Ollama
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=llama3.2
LLM_API_KEY=ollama  # Не требуется, но нужно для совместимости
```

### 3. Запуск агента

```bash
python main.py
```

---

## ⚙️ Настройка провайдеров

### Ollama

**Установка:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Доступные модели:**
- `llama3.2` - Llama 3.2 (3B/1B)
- `llama3.1` - Llama 3.1 (8B/70B/405B)
- `qwen2.5` - Qwen 2.5 (0.5B-72B)
- `mistral` - Mistral 7B
- `codellama` - Code Llama
- `deepseek-coder` - DeepSeek Coder

**Загрузка модели:**
```bash
ollama pull llama3.2
```

**Конфигурация .env:**
```env
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=llama3.2
LLM_API_KEY=ollama
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=4096
```

**Проверка работы:**
```bash
curl http://localhost:11434/v1/models
```

---

### LM Studio

**Установка:**
1. Скачайте с [lmstudio.ai](https://lmstudio.ai)
2. Установите и запустите
3. Загрузите модель через GUI
4. Включите "Local Server" в настройках

**Конфигурация .env:**
```env
LLM_PROVIDER=lmstudio
LLM_BASE_URL=http://localhost:1234/v1
LLM_MODEL=local-model
LLM_API_KEY=lm-studio
```

**Рекомендуемые модели:**
- `TheBloke/Llama-2-7B-Chat-GGUF`
- `TheBloke/Mistral-7B-Instruct-v0.2-GGUF`
- `TheBloke/CodeLlama-7B-Instruct-GGUF`

---

### LocalAI

**Установка через Docker:**
```bash
docker run -p 8080:8080 \
  -v $PWD/models:/models \
  quay.io/go-skynet/local-ai:latest
```

**Конфигурация .env:**
```env
LLM_PROVIDER=localai
LLM_BASE_URL=http://localhost:8080/v1
LLM_MODEL=gpt-3.5-turbo
LLM_API_KEY=local-ai
```

---

### vLLM

**Установка:**
```bash
pip install vllm
```

**Запуск сервера:**
```bash
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --port 8000
```

**Конфигурация .env:**
```env
LLM_PROVIDER=vllm
LLM_BASE_URL=http://localhost:8000/v1
LLM_MODEL=meta-llama/Llama-3.2-3B-Instruct
LLM_API_KEY=vllm
```

---

### Text Generation WebUI (oobabooga)

**Установка:**
```bash
git clone https://github.com/oobabooga/text-generation-webui
cd text-generation-webui
./start_linux.sh
```

**Включение OpenAI API:**
1. Запустите WebUI
2. Перейдите в "Session" → "Extensions"
3. Включите "openai" extension
4. API будет доступен на `http://localhost:5000`

**Конфигурация .env:**
```env
LLM_PROVIDER=textgen
LLM_BASE_URL=http://localhost:5000/v1
LLM_MODEL=text-generation-webui
LLM_API_KEY=textgen
```

⚠️ **Внимание:** Text Generation WebUI может не поддерживать function calling. Агент будет работать в ограниченном режиме.

---

## 📝 Примеры конфигураций

### Пример 1: OpenAI (облако)

```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4
```

### Пример 2: OpenRouter (облако)

```env
LLM_PROVIDER=openrouter
LLM_API_KEY=sk-or-v1-...
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=anthropic/claude-3.5-sonnet
```

### Пример 3: Ollama (локально)

```env
LLM_PROVIDER=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=llama3.2
LLM_API_KEY=ollama
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=4096
LLM_TIMEOUT=300
```

### Пример 4: LM Studio (локально)

```env
LLM_PROVIDER=lmstudio
LLM_BASE_URL=http://localhost:1234/v1
LLM_MODEL=local-model
LLM_API_KEY=lm-studio
```

### Пример 5: Кастомный провайдер

Если ваш провайдер не в списке, но поддерживает OpenAI API:

```env
LLM_PROVIDER=openai  # Используйте openai как базовый
LLM_API_KEY=your-key
LLM_BASE_URL=http://your-server:port/v1
LLM_MODEL=your-model
```

---

## 🔧 Дополнительные параметры

### Температура генерации

```env
LLM_TEMPERATURE=0.1  # 0.0 = детерминированный, 1.0 = креативный
```

### Максимальное количество токенов

```env
LLM_MAX_TOKENS=4096  # Максимальная длина ответа
```

### Таймаут запроса

```env
LLM_TIMEOUT=300  # Секунды (важно для медленных локальных моделей)
```

### Максимальное количество итераций

```env
MAX_ITERATIONS=20  # Количество шагов агента
```

---

## 🐛 Troubleshooting

### Проблема: "Connection refused"

**Решение:**
1. Убедитесь, что сервер запущен
2. Проверьте правильность URL и порта
3. Проверьте firewall

```bash
# Проверка доступности
curl http://localhost:11434/v1/models
```

### Проблема: "Model not found"

**Решение:**
1. Убедитесь, что модель загружена
2. Проверьте правильность имени модели

```bash
# Для Ollama
ollama list
ollama pull llama3.2
```

### Проблема: Медленная работа

**Решение:**
1. Используйте меньшую модель (3B вместо 70B)
2. Увеличьте `LLM_TIMEOUT`
3. Используйте квантизированные модели (GGUF Q4/Q5)
4. Убедитесь, что используется GPU

```bash
# Проверка GPU для Ollama
ollama run llama3.2 --verbose
```

### Проблема: Function calling не работает

**Решение:**
1. Убедитесь, что модель поддерживает function calling
2. Используйте модели с поддержкой tools:
   - Llama 3.1/3.2
   - Qwen 2.5
   - Mistral
3. Для старых моделей агент будет работать в ограниченном режиме

### Проблема: Out of memory

**Решение:**
1. Используйте меньшую модель
2. Используйте квантизацию (Q4_K_M вместо F16)
3. Уменьшите `LLM_MAX_TOKENS`
4. Закройте другие приложения

---

## 💡 Рекомендации

### Для начинающих
- **Ollama** + **Llama 3.2 3B** - простая установка, хорошее качество

### Для разработчиков
- **LM Studio** - удобный GUI, легко переключать модели

### Для продакшена
- **vLLM** - высокая производительность, batch processing

### Для экспериментов
- **LocalAI** - поддержка множества форматов моделей

---

## 📊 Сравнение моделей

| Модель | Размер | RAM | Качество | Function Calling |
|--------|--------|-----|----------|------------------|
| Llama 3.2 1B | 1B | 2GB | ⭐⭐⭐ | ✅ |
| Llama 3.2 3B | 3B | 4GB | ⭐⭐⭐⭐ | ✅ |
| Llama 3.1 8B | 8B | 8GB | ⭐⭐⭐⭐⭐ | ✅ |
| Qwen 2.5 7B | 7B | 8GB | ⭐⭐⭐⭐⭐ | ✅ |
| Mistral 7B | 7B | 8GB | ⭐⭐⭐⭐ | ✅ |
| DeepSeek Coder 6.7B | 6.7B | 8GB | ⭐⭐⭐⭐⭐ | ✅ |

---

## 🔐 Безопасность

При работе с локальными LLM:
- ✅ Данные не покидают ваш компьютер
- ✅ Полный контроль над моделью
- ✅ Нет ограничений по запросам
- ✅ Бесплатно после установки

---

## 📚 Дополнительные ресурсы

- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [LM Studio Docs](https://lmstudio.ai/docs)
- [LocalAI Documentation](https://localai.io/basics/getting_started/)
- [vLLM Documentation](https://docs.vllm.ai/)
- [Hugging Face Models](https://huggingface.co/models)

---

## 🆘 Поддержка

Если у вас возникли проблемы:
1. Проверьте [Troubleshooting](#troubleshooting)
2. Создайте issue на GitHub
3. Напишите в [Telegram](https://t.me/itpolice)

---

**Удачи в работе с локальными LLM! 🚀**
