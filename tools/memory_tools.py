"""
Инструменты для работы с долговременной памятью агента.
"""

from typing import Dict, Any
from memory import MemoryManager
import asyncio


# Глобальный экземпляр менеджера памяти
_memory_manager = None


def get_memory_manager() -> MemoryManager:
    """Получает глобальный экземпляр менеджера памяти."""
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = MemoryManager()
    return _memory_manager


async def memory_save_fact(content: str, category: str = "general") -> Dict[str, Any]:
    """Сохраняет важный факт в долговременную память."""
    try:
        manager = get_memory_manager()
        fact_id = await manager.add_fact(content, category)
        return {
            "success": True,
            "fact_id": fact_id,
            "message": f"Факт сохранён в категории '{category}' с ID {fact_id}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def memory_search(query: str, limit: int = 5) -> Dict[str, Any]:
    """Ищет релевантную информацию в памяти."""
    try:
        manager = get_memory_manager()
        results = await manager.search_facts(query, limit=limit)
        
        if not results:
            return {
                "success": True,
                "results": [],
                "message": "Релевантной информации не найдено"
            }
        
        formatted_results = []
        for r in results:
            formatted_results.append({
                "content": r["content"],
                "category": r["category"],
                "importance": r["importance"],
                "similarity": round(r["similarity"], 3)
            })
        
        return {
            "success": True,
            "results": formatted_results,
            "count": len(formatted_results)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def memory_get_summary() -> Dict[str, Any]:
    """Получает статистику по памяти агента."""
    try:
        manager = get_memory_manager()
        summary = await manager.get_memory_summary()
        return {"success": True, **summary}
    except Exception as e:
        return {"success": False, "error": str(e)}


async def memory_cleanup(days: int = 30) -> Dict[str, Any]:
    """Очищает устаревшие данные из памяти."""
    try:
        manager = get_memory_manager()
        result = await manager.cleanup_old_data(days_threshold=days)
        return {
            "success": True,
            "deleted_facts": result["deleted_facts"],
            "deleted_conversations": result["deleted_conversations"],
            "message": f"Удалено {result['deleted_facts']} фактов и {result['deleted_conversations']} диалогов старше {days} дней"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
