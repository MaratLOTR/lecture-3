"""Собрать автономные HTML-шпаргалки: python3 tools/build_cheatsheets.py.

Источники: README, TASK.md, docs/*.svg, реализация, демо, заготовка и тесты паттерна.
Генератор поддерживает разметку, используемую в этих README; внешних библиотек нет.
Правьте исходники, затем пересобирайте HTML. Запускать можно из любой папки.
"""

from html import escape
from pathlib import Path
import re
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent.parent
PATTERNS = {
    "adapter": ("Adapter — Адаптер", "devices.py", "adapter_thermostat.py"),
    "facade": ("Facade — Фасад", "home.py", "facade_night_mode.py"),
    "composite": ("Composite — Компоновщик", "tree.py", "composite_power_usage.py"),
    "bridge": ("Bridge — Мост · самостоятельно", "remotes.py", "bridge_limited_remote.py"),
}
TOKEN = re.compile(r"`([^`]+)`|\*\*(.+?)\*\*|\[([^\]]+)\]\(([^)]+)\)")
LIST_ITEM = re.compile(r"^(-|\d+\.)\s+(.+)")


def inline(text: str, link_prefix: str = "../") -> str:
    parts = []
    offset = 0
    for match in TOKEN.finditer(text):
        parts.append(escape(text[offset:match.start()]))
        code, bold, label, target = match.groups()
        if code is not None:
            parts.append(f"<code>{escape(code)}</code>")
        elif bold is not None:
            parts.append(f"<strong>{inline(bold, link_prefix)}</strong>")
        elif urlsplit(target).scheme in ("", "http", "https"):
            href = target if urlsplit(target).scheme or target.startswith("#") else link_prefix + target
            parts.append(f'<a href="{escape(href, quote=True)}">{inline(label, link_prefix)}</a>')
        else:
            parts.append(escape(label))
        offset = match.end()
    parts.append(escape(text[offset:]))
    return "".join(parts)


def render_markdown(text: str) -> str:
    """Абзацы, заголовки, таблицы, списки и блоки кода из README проекта."""
    lines = text.splitlines()
    result = []
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip():
            continue
        if line.startswith("```"):
            code = []
            while index < len(lines) and not lines[index].startswith("```"):
                code.append(lines[index])
                index += 1
            index += 1
            result.append(f"<pre><code>{escape(chr(10).join(code))}</code></pre>")
        elif heading := re.match(r"^(#{1,6}) (.+)", line):
            level = len(heading[1])
            result.append(f"<h{level}>{inline(heading[2])}</h{level}>")
        elif line.startswith("|"):
            rows = [line]
            while index < len(lines) and lines[index].startswith("|"):
                rows.append(lines[index])
                index += 1
            table = []
            for row in rows:
                cells = [cell.strip() for cell in row.strip("|").split("|")]
                if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                    continue
                tag = "th" if not table else "td"
                table.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>")
            result.append('<div class="scroll"><table>' + "".join(table) + "</table></div>")
        elif item := LIST_ITEM.match(line):
            tag = "ul" if item[1] == "-" else "ol"
            items = []
            while item:
                body = [item[2]]
                while index < len(lines) and lines[index].startswith("  ") and lines[index].strip():
                    body.append(lines[index].strip())
                    index += 1
                items.append(f"<li>{inline(' '.join(body))}</li>")
                item = LIST_ITEM.match(lines[index]) if index < len(lines) else None
                if item and (item[1] == "-") == (tag == "ul"):
                    index += 1
                else:
                    break
            result.append(f"<{tag}>{''.join(items)}</{tag}>")
        else:
            paragraph = [line]
            while index < len(lines) and lines[index].strip():
                if lines[index].startswith(("#", "```", "|")) or LIST_ITEM.match(lines[index]):
                    break
                paragraph.append(lines[index])
                index += 1
            result.append(f"<p>{inline(' '.join(paragraph))}</p>")
    return "\n".join(result)


CSS = """
:root{color-scheme:light;font:17px/1.65 system-ui,-apple-system,sans-serif;color:#203640;background:#fafbf9}
*{box-sizing:border-box}body{margin:0}main{max-width:1060px;margin:auto;padding:32px 24px 70px}
nav{display:flex;flex-wrap:wrap;gap:12px 24px;border-bottom:1px solid #ccd7da;padding-bottom:18px}
a{color:#176579;text-underline-offset:3px}nav [aria-current]{font-weight:750;color:#203640}
h1{font:700 clamp(30px,5vw,48px)/1.2 Georgia,serif;margin:40px 0 26px}
h2{font:650 29px/1.3 Georgia,serif;margin:44px 0 18px}h3{margin:25px 0 12px}
p,li{max-width:78ch}li{margin:6px 0}code{font:0.88em ui-monospace,monospace}
pre{padding:18px;background:#edf2f3;border:1px solid #d7e1e4;overflow:auto;line-height:1.6}
pre code{white-space:pre}p code,li code,td code{overflow-wrap:anywhere}
.scroll,.diagram{overflow:auto}table{width:100%;border-collapse:collapse;font-size:15px}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid #ccd7da}th{background:#eef3f3}
.diagram img{display:block;width:100%;min-width:700px;height:auto;border:1px solid #d7e1e4}
figure{margin:20px 0 30px}figcaption{margin-top:8px;color:#526970;font-size:15px}
details{margin:18px 0;border-top:1px solid #ccd7da;padding-top:14px}summary{cursor:pointer;font-weight:650}
button{font:inherit;font-size:14px;padding:6px 12px;background:#fff;border:1px solid #78939e;cursor:pointer;margin-top:14px}
button:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid #257f99;outline-offset:4px}
.status{margin-left:12px;font-size:14px}.note{border-left:4px solid #3b8190;padding:10px 18px;background:#edf4f3}
footer{margin-top:50px;border-top:1px solid #ccd7da;padding-top:18px;color:#526970}
@media(max-width:600px){main{padding:20px 15px}pre{font-size:14px}h2{font-size:25px}}
@media print{nav,button,.status{display:none}main{max-width:none;padding:0}body{background:#fff}pre{white-space:pre-wrap;overflow:visible;font-size:10px}pre code{white-space:pre-wrap}details{break-inside:avoid}.diagram img{min-width:0}h2,h3{break-after:avoid}}
"""

SCRIPT = """
document.querySelectorAll('.copy').forEach(button => {
  button.addEventListener('click', async () => {
    const code = button.parentElement.querySelector('code');
    const status = button.nextElementSibling;
    try {
      await navigator.clipboard.writeText(code.textContent);
      status.textContent = 'Скопировано';
    } catch {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges(); selection.addRange(range);
      status.textContent = 'Код выделен. Нажмите Ctrl+C или ⌘C.';
    }
  });
});
window.addEventListener('beforeprint', () => {
  document.querySelectorAll('details').forEach(item => {
    item.dataset.wasOpen = String(item.open); item.open = true;
  });
});
window.addEventListener('afterprint', () => {
  document.querySelectorAll('details').forEach(item => {
    item.open = item.dataset.wasOpen === 'true';
  });
});
"""


def code_block(path: Path, label: str) -> str:
    return (
        f'<details open><summary>{escape(label)}</summary>'
        '<button type="button" class="copy">Копировать код</button>'
        '<span class="status" role="status"></span>'
        f'<pre><code>{escape(path.read_text(encoding="utf-8"))}</code></pre></details>'
    )


def build(pattern: str, root: Path = ROOT) -> str:
    title, source, exercise = PATTERNS[pattern]
    base = root / "patterns" / pattern
    nav = "".join(
        f'<a href="../../{name}/docs/cheatsheet.html"'
        + (' aria-current="page"' if name == pattern else "")
        + f'>{escape(info[0])}</a>'
        for name, info in PATTERNS.items()
    )
    diagrams = "".join(
        '<figure><div class="diagram">'
        f'<img src="data:image/svg+xml;charset=utf-8,{svg_data(base / "docs" / filename)}" '
        f'alt="{caption}"></div><figcaption>{caption}</figcaption></figure>'
        for filename, caption in (
            ("classes.svg", "UML: диаграмма классов"),
            ("sequence.svg", "UML: последовательность вызовов"),
        )
    )
    content = render_markdown((base / "README.md").read_text(encoding="utf-8"))
    content += render_markdown((base / "TASK.md").read_text(encoding="utf-8"))
    code = code_block(base / source, f"Реализация: {source}")
    code += code_block(base / "__main__.py", "Демонстрация: __main__.py")
    code += code_block(base / exercise, f"Дополнительное задание: {exercise}")
    for filename in ("test_example.py", "test_task.py", "test_extra.py"):
        code += code_block(base / "tests" / filename, f"Тесты: tests/{filename}")
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · Умный дом</title><link rel="icon" href="data:,"><style>{CSS}</style></head>
<body><main><nav aria-label="Паттерны">{nav}</nav>
<p class="note">Умный дом · Python 3.10+ · pytest 9+ для тестов · Материал и диаграммы доступны без интернета.
Bridge — дополнительный раздел для самостоятельного изучения.</p>
{content}
<h2 id="uml">UML-диаграммы</h2>{diagrams}
<h2 id="code">Код и дополнительная практика</h2>
<p>Заготовка с TODO проверяется отдельно от работающих примеров.
Команды и порядок выполнения — в <a href="../TASK.md">описании задания этого паттерна</a>.</p>
{code}
<footer>Страница собрана из исходников проекта.
После изменений выполните <code>python3 tools/build_cheatsheets.py</code>.
Диаграммы и код встроены в этот HTML; для перехода к другим паттернам сохраните папку проекта целиком.</footer>
</main><script>{SCRIPT}</script></body></html>'''


def svg_data(path: Path) -> str:
    from urllib.parse import quote

    return quote(path.read_text(encoding="utf-8"), safe="")


def main() -> None:
    for pattern in PATTERNS:
        target = ROOT / "patterns" / pattern / "docs" / "cheatsheet.html"
        target.write_text(build(pattern), encoding="utf-8")
        print(f"Готово: {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
