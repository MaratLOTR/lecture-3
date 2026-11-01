from html.parser import HTMLParser
import unittest

from tools.build_cheatsheets import PATTERNS, build, render_markdown


class ResourceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.external_resources = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "img":
            self.images.append(values.get("src", ""))
        if tag in ("script", "img", "link"):
            target = values.get("src", values.get("href", ""))
            if target.startswith(("http:", "https:", "//")):
                self.external_resources.append(target)


class CheatsheetTests(unittest.TestCase):
    def test_code_is_preserved_as_text_and_html_is_escaped(self):
        rendered = render_markdown('```python\nprint("<script>&")\n```')
        self.assertIn('&lt;script&gt;&amp;', rendered)
        self.assertNotIn('<script>', rendered)
        self.assertIn('<pre><code>', rendered)

    def test_markdown_keeps_tables_lists_and_relative_links(self):
        rendered = render_markdown(
            '| Роль | Класс |\n|---|---|\n| Target | `Switchable` |\n\n'
            '1. **Первый** шаг\n   продолжение\n2. Второй шаг\n\n'
            '[Код](devices.py) и [опасная ссылка](javascript:alert)'
        )
        self.assertIn('<th>Роль</th>', rendered)
        self.assertIn('<code>Switchable</code>', rendered)
        self.assertIn('<li><strong>Первый</strong> шаг продолжение</li>', rendered)
        self.assertIn('href="../devices.py"', rendered)
        self.assertNotIn('href="javascript:', rendered)

    def test_all_pages_embed_diagrams_and_code_without_external_resources(self):
        for pattern, (_, source, exercise) in PATTERNS.items():
            with self.subTest(pattern=pattern):
                page = build(pattern)
                parser = ResourceParser()
                parser.feed(page)
                self.assertEqual(len(parser.images), 2)
                self.assertTrue(all(src.startswith('data:image/svg+xml;') for src in parser.images))
                self.assertEqual(parser.external_resources, [])
                self.assertIn(source, page)
                self.assertIn(exercise, page)
                self.assertIn('Тесты: tests/test_task.py', page)
                self.assertIn('Тесты: tests/test_extra.py', page)
                self.assertIn('без пропусков', page)
                self.assertIn('aria-current="page"', page)
