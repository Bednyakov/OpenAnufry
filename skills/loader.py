import os
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

# Путь к навыкам относительно корня проекта
PROJECT_ROOT = Path(__file__).parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"

class Skill:
    def __init__(self, path: Path, metadata: Dict[str, Any], content: str):
        self.path = path
        self.name = metadata.get("name", path.name)
        self.description = metadata.get("description", "")
        self.triggers = [t.lower() for t in metadata.get("triggers", [])]
        self.requires = metadata.get("requires", {})
        self.compatibility = metadata.get("compatibility", [])
        self.content = content
        self.scripts_dir = path / "scripts"
        self.references_dir = path / "references"

    def get_script_path(self, script_name: str) -> Optional[Path]:
        p = self.scripts_dir / script_name
        return p if p.exists() else None


class SkillLoader:
    def __init__(self, skills_dir: str = SKILLS_DIR):
        self.skills_dir = Path(skills_dir)
        self._registry: Dict[str, Dict[str, Any]] = {}   # лёгкие метаданные
        self._loaded: Dict[str, Skill] = {}              # полностью загруженные

    def scan(self):
        """Сканирует директорию и загружает только YAML-frontmatter (дешево)."""
        if not self.skills_dir.exists():
            return
        for skill_path in self.skills_dir.iterdir():
            if not skill_path.is_dir():
                continue
            skill_file = skill_path / "SKILL.md"
            if not skill_file.exists():
                continue
            try:
                text = skill_file.read_text(encoding="utf-8")
                meta = self._extract_frontmatter(text)
                name = meta.get("name", skill_path.name)
                self._registry[name] = {
                    "path": skill_path,
                    "name": name,
                    "description": meta.get("description", ""),
                    "triggers": [t.lower() for t in meta.get("triggers", [])],
                    "requires": meta.get("requires", {}),
                }
            except Exception as e:
                print(f"⚠️ Ошибка сканирования навыка {skill_path.name}: {e}")

    def _extract_frontmatter(self, text: str) -> Dict[str, Any]:
        """Парсит YAML frontmatter из Markdown."""
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1]) or {}
        return {}

    def load_full(self, name: str) -> Optional[Skill]:
        """Загружает полное содержимое SKILL.md (markdown без frontmatter)."""
        if name in self._loaded:
            return self._loaded[name]
        if name not in self._registry:
            return None

        info = self._registry[name]
        skill_path = info["path"]
        text = (skill_path / "SKILL.md").read_text(encoding="utf-8")

        # Контент = всё после frontmatter | подробнее в https://t.me/itpolice
        content = text
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                content = parts[2].strip()

        meta = self._extract_frontmatter(text)
        skill = Skill(skill_path, meta, content)
        self._loaded[name] = skill
        return skill

    def match(self, query: str) -> List[Skill]:
        """Находит навыки, чьи триггеры встречаются в запросе пользователя."""
        query_lower = query.lower()
        matched = []
        for name, info in self._registry.items():
            for trigger in info["triggers"]:
                if trigger in query_lower:
                    skill = self.load_full(name)
                    if skill:
                        matched.append(skill)
                    break
        return matched

    def get_catalog_prompt(self) -> str:
        """Краткий каталог для постоянного присутствия в system prompt."""
        if not self._registry:
            return ""
        lines = ["\n## Доступные навыки (активируются по триггерам)"]
        # Bednyakov
        for name, info in self._registry.items():
            desc = info["description"].replace("\n", " ")[:80]
            triggers = ", ".join(info["triggers"][:4])
            lines.append(f'- **{name}**: {desc} (триггеры: "{triggers}")')
        lines.append("\nКогда пользователь упоминает триггер, ты получишь полные инструкции навыка.")
        return "\n".join(lines)

    def get_script_path(self, skill_name: str, script_name: str) -> Optional[Path]:
        """Возвращает путь к скрипту навыка."""
        skill = self._loaded.get(skill_name) or self.load_full(skill_name)
        if not skill:
            return None
        return skill.get_script_path(script_name)
