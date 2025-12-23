from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]  # .../src
APP = ROOT / "app"

IMPORT_RE = re.compile(r"^\s*(from\s+([a-zA-Z0-9_.]+)\s+import|import\s+([a-zA-Z0-9_.]+))")

def main() -> None:
    print("IMPORT MAP (very simple):\n")

    for py in sorted(APP.rglob("*.py")):
        rel = py.relative_to(ROOT)
        lines = py.read_text(encoding="utf-8", errors="ignore").splitlines()

        imports = []
        for line in lines:
            m = IMPORT_RE.match(line)
            if not m:
                continue
            mod = m.group(2) or m.group(3)
            # показываем только импорты внутри нашего проекта (app.*)
            if mod.startswith("app."):
                imports.append(mod)

        if imports:
            print(f"{rel}:")
            for imp in sorted(set(imports)):
                print(f"  -> {imp}")
            print()

if __name__ == "__main__":
    main()
