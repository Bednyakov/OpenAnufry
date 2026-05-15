import os
import subprocess
from typing import Dict, Any, List
from config import WORKSPACE_DIR
from skills.loader import SkillLoader

def run_skill_script(skill_loader: SkillLoader, skill_name: str, script_name: str,
                     args: List[str] = None, timeout: int = 60) -> Dict[str, Any]:
    """Выполняет скрипт из папки scripts/ конкретного навыка."""
    if args is None:
        args = []

    script_path = skill_loader.get_script_path(skill_name, script_name)
    if not script_path:
        return {
            "success": False,
            "error": f"Скрипт '{script_name}' не найден в навыке '{skill_name}'"
        }

    try:
        os.chmod(script_path, 0o755)
        result = subprocess.run(
            [str(script_path)] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=WORKSPACE_DIR
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
