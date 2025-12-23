from __future__ import annotations

from pathlib import Path
import re

from graphviz import Digraph

ROOT = Path(__file__).resolve().parents[2]  # .../src
APP = ROOT / "app"

IMPORT_RE = re.compile(r"^\s*(from\s+([a-zA-Z0-9_.]+)\s+import|import\s+([a-zA-Z0-9_.]+))")


def build_import_graph() -> Digraph:
    g = Digraph("job_radar_imports", format="png")
    g.attr(rankdir="LR", fontsize="10")

    for py in sorted(APP.rglob("*.py")):
        rel = py.relative_to(ROOT)
        module_name = "app." + ".".join(rel.with_suffix("").parts[1:])  # app.core.logging и т.п.

        g.node(module_name, module_name)

        lines = py.read_text(encoding="utf-8", errors="ignore").splitlines()

        for line in lines:
            m = IMPORT_RE.match(line)
            if not m:
                continue
            imported = m.group(2) or m.group(3)
            if not imported.startswith("app."):
                continue
            g.node(imported, imported)
            g.edge(module_name, imported)

    return g


def main() -> None:
    graph = build_import_graph()
    out_path = ROOT.parent / "docs" / "import_graph"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    filename = graph.render(str(out_path), cleanup=True)
    print("Graph saved to:", filename)


if __name__ == "__main__":
    main()
