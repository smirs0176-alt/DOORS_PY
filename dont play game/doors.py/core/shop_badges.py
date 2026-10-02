import os
import json
from core.display import Display, Colors
from core.items import Flashlight, Lockpick, Lighter, Pills

class BadgeManager:
    BADGES = {
        "first_death": {"name": "💀 Первая ошибка", "desc": "Умереть в первый раз"},
        "meet_architect": {"name": "💧 Границы разума", "desc": "Услышать усталость Водного Света"},
        "stairwell_runner": {"name": "🪜 Спуск в бездну", "desc": "Зайти на подэтаж The Stairwell"},
        "bleach_survivor": {"name": "🧪 Чистый разум", "desc": "Выжить после атаки Блича"},
        "rich_guy": {"name": "🪙 Богач", "desc": "Собрать 100 монет"}
    }

    @staticmethod
    def unlock_badge(badge_id: str):
        if badge_id not in BadgeManager.BADGES:
            return

        data = BadgeManager._load_data()
        if badge_id not in data.get("badges", []):
            data.setdefault("badges", []).append(badge_id)
            BadgeManager._save_data(data)
            badge = BadgeManager.BADGES[badge_id]
            print(f"\n{Colors.YELLOW}🏆 [НОВЫЙ БЕЙДЖ!] {badge['name']} — {badge['desc']}{Colors.RESET}")

    @staticmethod
    def show_badges():
        Display.clear_screen()
        data = BadgeManager._load_data()
        unlocked = data.get("badges", [])

        print(f"{Colors.CYAN}{Colors.BOLD}==========================================")
        print("            🏆 ВАШИ БЕЙДЖИ (АЧИВКИ)        ")
        print("==========================================" + Colors.RESET)

        for b_id, info in BadgeManager.BADGES.items():
            status = f"{Colors.GREEN}[ПОЛУЧЕНО]{Colors.RESET}" if b_id in unlocked else f"{Colors.RED}[ЗАКРЫТО]{Colors.RESET}"
            print(f"{status} {info['name']} — {info['desc']}")

        print(f"{Colors.CYAN}==========================================" + Colors.RESET)
        input("\nНажмите Enter, чтобы вернуться...")

    @staticmethod
    def _load_data():
        if os.path.exists("stats.json"):
            try:
                with open("stats.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"deaths": 0, "coins": 0, "badges": []}

    @staticmethod
    def _save_data(data):
        with open("stats.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


class Shop:
    @staticmethod
    def open_shop(player):
        data = BadgeManager._load_data()
        coins = data.get("coins", 50)  # Стартовый баланс

        while True:
            Display.clear_screen()
            print(f"{Colors.YELLOW}{Colors.BOLD}==========================================")
            print(f"            🏪 МАГАЗИН ДЖЕФФА             ")
            print(f"💰 Ваши монеты: {coins} 🪙")
            print("==========================================" + Colors.RESET)
            print("1. 🔦 Фонарик (30 монет)")
            print("2. 🗝️ Отмычки (25 монет)")
            print("3. 🔥 Поджигалочка (15 монет)")
            print("4. 💊 Таблеточки (20 монет)")
            print("0. ⬅️ Выйти из магазина")
            print("==========================================")

            choice = input("\nВыберите товар для покупки: ").strip()

            if choice == "1" and coins >= 30:
                coins -= 30
                player.add_item(Flashlight())
            elif choice == "2" and coins >= 25:
                coins -= 25
                player.add_item(Lockpick())
            elif choice == "3" and coins >= 15:
                coins -= 15
                player.add_item(Lighter())
            elif choice == "4" and coins >= 20:
                coins -= 20
                player.add_item(Pills())
            elif choice == "0":
                break
            else:
                input("\n❌ Недостаточно монет или неверный выбор! Нажмите Enter...")

        data["coins"] = coins
        BadgeManager._save_data(data)