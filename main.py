"""Запуск учебных примеров: python3 main.py [--bridge]."""

import argparse

from patterns.adapter.__main__ import demo as adapter_demo
from patterns.composite.__main__ import demo as composite_demo
from patterns.facade.__main__ import demo as facade_demo


def main() -> None:
    parser = argparse.ArgumentParser(description="Структурные паттерны: умный дом")
    parser.add_argument(
        "--bridge", action="store_true", help="добавить пример для самостоятельного изучения"
    )
    args = parser.parse_args()
    for demo in (adapter_demo, facade_demo, composite_demo):
        demo()
        print()
    if args.bridge:
        from patterns.bridge.__main__ import demo as bridge_demo

        bridge_demo()


if __name__ == "__main__":
    main()
