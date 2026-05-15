import asyncio
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright

_browser = None
_page = None

async def _ensure_browser():
    """Ленивая инициализация браузера."""
    global _browser, _page
    if _browser is None:
        playwright = await async_playwright().start()
        _browser = await playwright.chromium.launch(headless=True)
        _page = await _browser.new_page()
    return _page

async def browser_navigate(url: str) -> Dict[str, Any]:
    """Открывает URL в браузере."""
    page = await _ensure_browser()
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
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
        return {"success": True, "selector": selector}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def browser_type(selector: str, text: str) -> Dict[str, Any]:
    """Вводит текст в поле."""
    page = await _ensure_browser()
    try:
        await page.fill(selector, text)
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

async def browser_close() -> Dict[str, Any]:
    """Закрывает браузер."""
    global _browser
    if _browser:
        await _browser.close()
        _browser = None
    return {"success": True}
