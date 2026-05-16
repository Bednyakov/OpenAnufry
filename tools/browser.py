import asyncio
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright

_browser = None
_page = None
_playwright = None

async def _ensure_browser():
    """Ленивая инициализация браузера с антидетект настройками."""
    global _browser, _page, _playwright
    if _browser is None:
        _playwright = await async_playwright().start()
        
        # Запускаем браузер с настройками для обхода детекции
        _browser = await _playwright.chromium.launch(
            headless=False,  # Используем видимый браузер (можно переключить на True если нужно)
            args=[
                '--disable-blink-features=AutomationControlled',  # Отключаем флаг автоматизации
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
        )
        
        # Создаем контекст с дополнительными настройками
        context = await _browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='ru-RU',
            timezone_id='Europe/Moscow',
            permissions=['geolocation']
        )
        
        _page = await context.new_page()
        
        # Скрываем признаки автоматизации
        await _page.add_init_script("""
            // Переопределяем webdriver
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            });
            
            // Добавляем chrome объект
            window.chrome = {
                runtime: {}
            };
            
            // Переопределяем permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Добавляем плагины
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Добавляем языки
            Object.defineProperty(navigator, 'languages', {
                get: () => ['ru-RU', 'ru', 'en-US', 'en']
            });
        """)
    
    return _page

async def browser_navigate(url: str) -> Dict[str, Any]:
    """Открывает URL в браузере."""
    page = await _ensure_browser()
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Небольшая задержка для имитации человеческого поведения
        await asyncio.sleep(1)
        
        title = await page.title()
        return {
            "success": True,
            "url": page.url,
            "title": title,
            "content_length": len(await page.content())
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

async def browser_click(selector: str) -> Dict[str, Any]:
    """Кликает по элементу."""
    page = await _ensure_browser()
    try:
        await page.click(selector, timeout=10000)
        await asyncio.sleep(0.5)  # Имитация человеческого поведения
        return {"success": True, "selector": selector}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def browser_type(selector: str, text: str) -> Dict[str, Any]:
    """Вводит текст в поле."""
    page = await _ensure_browser()
    try:
        await page.fill(selector, text)
        await asyncio.sleep(0.3)  # Имитация человеческого поведения
        return {"success": True, "selector": selector, "text": text}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def browser_get_text(selector: str = "body") -> Dict[str, Any]:
    """Получает текст элемента."""
    page = await _ensure_browser()
    try:
        text = await page.inner_text(selector)
        return {"success": True, "text": text[:5000]}  # Лимит для контекста
    except Exception as e:
        return {"success": False, "error": str(e)}

async def browser_screenshot(path: str = "screenshot.png") -> Dict[str, Any]:
    """Делает скриншот."""
    page = await _ensure_browser()
    try:
        await page.screenshot(path=path, full_page=True)
        return {"success": True, "path": path}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def browser_search_google(query: str) -> Dict[str, Any]:
    """
    Выполняет поиск в Google и возвращает результаты.
    Использует антидетект меры для обхода блокировок.
    """
    page = await _ensure_browser()
    try:
        # Переходим на Google
        await page.goto("https://www.google.com", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(1)
        
        # Ищем поле поиска и вводим запрос
        search_input = await page.query_selector('textarea[name="q"], input[name="q"]')
        if search_input:
            await search_input.type(query, delay=100)  # Имитация печати человека
            await asyncio.sleep(0.5)
            await search_input.press("Enter")
            
            # Ждем загрузки результатов
            await page.wait_for_load_state("networkidle", timeout=15000)
            await asyncio.sleep(2)
            
            # Извлекаем результаты поиска
            results = []
            search_results = await page.query_selector_all('div.g, div[data-sokoban-container]')
            
            for result in search_results[:10]:  # Берем первые 10 результатов
                try:
                    title_elem = await result.query_selector('h3')
                    link_elem = await result.query_selector('a')
                    snippet_elem = await result.query_selector('div[data-sncf], div.VwiC3b, span.aCOpRe')
                    
                    if title_elem and link_elem:
                        title = await title_elem.inner_text()
                        link = await link_elem.get_attribute('href')
                        snippet = await snippet_elem.inner_text() if snippet_elem else ""
                        
                        results.append({
                            "title": title,
                            "link": link,
                            "snippet": snippet
                        })
                except Exception:
                    continue
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "count": len(results)
            }
        else:
            return {"success": False, "error": "Не удалось найти поле поиска"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

async def browser_close() -> Dict[str, Any]:
    """Закрывает браузер."""
    global _browser, _playwright
    if _browser:
        await _browser.close()
        _browser = None
    if _playwright:
        await _playwright.stop()
        _playwright = None
    return {"success": True}
