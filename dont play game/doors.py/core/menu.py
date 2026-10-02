import os
import json
from core.display import Display, Colors
from core.shop_badges import BadgeManager, Shop
from core.player import Player

class MainMenu:
    @staticmethod
    def show() -> str:
        """Главное меню игры с переходами по окнам."""
        while True:
            Display.clear_screen()
            Display.show_logo()

            print(f"{Colors.WHITE}{Colors.BOLD}┌──────────────────────────────────────────┐")
            print("│               ГЛАВНОЕ МЕНЮ               │")
            print("├──────────────────────────────────────────┤")
            print("│ 1. 🏨 Начать заезд (The Hotel)          │")
            print("│ 2. 🌀 Выбор локации / Подэтажа           │")
            print("│ 3. 🏪 Магазин Джеффа                    │")
            print("│ 4. 🏆 Ваши Бейджи и Ачивки              │")
            print("│ 5. 💀 Статистика смертей                │")
            print("│ 6. 📜 Авторы и О проекте                 │")
            print("│ 0. 🚪 Выйти из игры                      │")
            print(f"└──────────────────────────────────────────┘{Colors.RESET}")

            choice = input(f"\n{Colors.YELLOW}Выберите действие (0-6): {Colors.RESET}").strip()

            if choice == "1":
                return "start_hotel"
            elif choice == "2":
                floor_choice = MainMenu.show_floor_selector()
                if floor_choice:
                    return floor_choice
            elif choice == "3":
                # Запуск Магазина
                temp_player = Player()
                Shop.open_shop(temp_player)
            elif choice == "4":
                # Экран Бейджей
                BadgeManager.show_badges()
            elif choice == "5":
                # Экран Статистики
                MainMenu.show_stats_screen()
            elif choice == "6":
                # Экран Авторов
                MainMenu.show_about_screen()
            elif choice == "0":
                return "exit"
            else:
                input(f"\n{Colors.RED}❌ Неверный ввод! Нажмите Enter для повтора...{Colors.RESET}")

    @staticmethod
    def show_floor_selector() -> str:
        """Экран выбора локаций и секретных подэтажей."""
        while True:
            Display.clear_screen()
            print(f"{Colors.CYAN}{Colors.BOLD}")
            print("┌──────────────────────────────────────────┐")
            print("│          🏢 ВЫБОР ЭТАЖА / ЛОКАЦИИ        │")
            print("├──────────────────────────────────────────┤")
            print("│ 1. 🏨 The Hotel (Комнаты 1–100)          │")
            print("│ 2. 🚪 The Rooms (Подэтаж: A-001 - A-1000)│")
            print("│ 3. 🪜 The Stairwell (Бесконечный спуск)  │")
            print("│ 0. ⬅️ Назад в Главное Меню               │")
            print("└──────────────────────────────────────────┘" + Colors.RESET)

            choice = input(f"\n{Colors.YELLOW}Выберите локацию (0-3): {Colors.RESET}").strip()
            if choice == "1":
                return "start_hotel"
            elif choice == "2":
                return "start_rooms"
            elif choice == "3":
                return "start_stairwell"
            elif choice == "0":
                return None
            else:
                input(f"\n{Colors.RED}❌ Неверная локация! Нажмите Enter...{Colors.RESET}")

    @staticmethod
    def show_stats_screen():
        """Экран статистики смертей."""
        Display.clear_screen()
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("==========================================")
        print("          💀 СТАТИСТИКА ИГРОКА            ")
        print("==========================================")
        
        deaths = 0
        if os.path.exists("stats.json"):
            try:
                with open("stats.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    deaths = data.get("deaths", 0)
            except Exception:
                deaths = 0

        print(f"📊 Всего погиб от монстров: {deaths} раз(а)")
        print("\n💧 Водный Свет помнит каждую твою ошибку...")
        print("==========================================" + Colors.RESET)
        input(f"\n{Colors.YELLOW}Нажмите Enter, чтобы вернуться...{Colors.RESET}")

    @staticmethod
    def show_about_screen():
        """Экран информации с авторами и описанием."""
        Display.clear_screen()
        print(f"{Colors.GREEN}{Colors.BOLD}")
        print("==========================================")
        print("          📜 О ПРОЕКТЕ DOORS TEXT         ")
        print("==========================================")
        print("👑 Главный создатель: rubrub46")
        print("💡 Идея взята из проекта LSplash (DOORS на платформе Roblox)")
        print("------------------------------------------")
        print("🏛️ Локации: The Hotel, The Rooms (A-000), The Stairwell")
        print("👹 Монстры: Drush, Reys, Seek, A-60, A-90, A-120, Crash, Brush, Bleach")
        print("💧 Архитектор: Водный Свет")
        print("------------------------------------------")
        print("🎮 Создано по мотивам игры Roblox DOORS")
        print("🐍 Эта игра создана на чистом Пайтоне!")
        print("==========================================" + Colors.RESET)
        input(f"\n{Colors.YELLOW}Нажмите Enter, чтобы вернуться...{Colors.RESET}")