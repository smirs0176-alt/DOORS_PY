import os
import time
import json
import importlib
import config
from core.player import Player
from core.room import Room
from core.events import EventManager
from core.floors import FloorManager

class GameEngine:
    def __init__(self):
        self.player = Player()
        self.current_room_number = 0
        self.entities = []
        self.architect = None
        self.death_count = self._load_death_count()
        self.load_entities()

    def _load_death_count(self) -> int:
        """Загружает общую статистику смертей из файла stats.json."""
        if os.path.exists("stats.json"):
            try:
                with open("stats.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("deaths", 0)
            except Exception:
                return 0
        return 0

    def _save_death_count(self):
        """Сохраняет обновленный счётчик смертей."""
        with open("stats.json", "w", encoding="utf-8") as f:
            json.dump({"deaths": self.death_count}, f, ensure_ascii=False, indent=4)

    def load_entities(self):
        """Динамическая загрузка монстров и Водного Света из папки entities/."""
        self.entities.clear()
        self.architect = None
        entities_dir = "entities"
        
        if not os.path.exists(entities_dir):
            os.makedirs(entities_dir)

        for filename in os.listdir(entities_dir):
            if filename.endswith(".py") and filename != "base_entity.py":
                module_name = f"{entities_dir}.{filename[:-3]}"
                module = importlib.import_module(module_name)
                importlib.reload(module)
                
                if hasattr(module, "setup"):
                    entity_instance = module.setup()
                    # Отделяем Водный Свет (Архитектора) от стандартных монстров
                    if "Водный Свет" in entity_instance.name or "Архитектор" in entity_instance.name:
                        self.architect = entity_instance
                    else:
                        self.entities.append(entity_instance)

    def handle_player_death(self, cause_of_death: str = "Неизвестная опасность"):
        """Обработка гибели игрока: увеличивает счетчик и вызывает Водный Свет."""
        self.death_count += 1
        self._save_death_count()
        
        if self.architect:
            self.architect.give_death_message(self.death_count, cause_of_death)
        else:
            print(f"\n💀 ВЫ УМЕРЛИ! Всего смертей: {self.death_count}")

    def play_turn(self) -> bool:
        """Основной цикл прохождения комнат The Hotel."""
        self.current_room_number += 1
        room = Room(self.current_room_number)
        self.player.is_hiding = False

        # -------------------------------------------------------------
        # КАСТОМНЫЕ СОБЫТИЯ И СЕКРЕТНЫЕ ПЕРЕХОДЫ
        # -------------------------------------------------------------

        # 1. Первый побег от Сика (35–40 комнаты)
        if self.current_room_number == 35:
            survived = EventManager.run_seek_chase(self.player, 35, total_chase_rooms=5)
            if not survived:
                self.handle_player_death("Сик (Первая погоня)")
                return False
            self.current_room_number = 40
            return True

        # 2. Нубини/Нубинька в Библиотеке (50 комната)
        if self.current_room_number == 50:
            survived = EventManager.run_nubini_library(self.player)
            if not survived:
                self.handle_player_death("Нубинька (Библиотека)")
                return False
            return True

        # 3. Секретный переход за шкафом в The Rooms (60 комната)
        if self.current_room_number == 60:
            print("\n" + "🔍" * 25)
            print("🚪 КОМНАТА 60: Вы заметили, что тяжелый шкаф стоит под углом...")
            print("За ним скрывается массивная металлическая дверь с надписью A-000!")
            choice = input("Отодвинуть шкаф и попытаться войти в The Rooms? (да/нет): ").strip().lower()
            
            if choice == "да":
                has_lockpick = any(item.name == "Отмычки" for item in self.player.inventory)
                if has_lockpick:
                    print("🔓 Вы с треском взломали замок A-000 отмычкой!")
                    return FloorManager.enter_the_rooms(self.player)
                else:
                    print("🔒 Дверь A-000 заперта! Нужны Отмычки в инвентаре.")
                    print("Вы вздохнули и пошли дальше по коридору Отеля.")

        # 4. Второй усложнённый побег от Сика (70–80 комнаты)
        if self.current_room_number == 70:
            survived = EventManager.run_seek_chase(self.player, 70, total_chase_rooms=10)
            if not survived:
                self.handle_player_death("Сик (Вторая погоня)")
                return False
            self.current_room_number = 80
            return True

        # 5. Оранжерея (90–99 комнаты): Всплеск активности Драша
        if 90 <= self.current_room_number <= 99:
            print("\n🌿 [ОРАНЖЕРЕЯ] Плотный туман, стебли и шум вентиляции... Драш где-то рядом!")
            for entity in self.entities:
                if entity.name == "Drush":
                    entity.spawn_chance = 0.65

        # 6. Финал: Электрощитовая (100 комната)
        if self.current_room_number == 100:
            survived = EventManager.run_final_room_100(self.player)
            if not survived:
                self.handle_player_death("Замыкание током (100-я комната)")
                return False
            return True

        # -------------------------------------------------------------
        # ОБЫЧНАЯ КОМНАТА
        # -------------------------------------------------------------
        print(f"\n==================================================")
        print(f"❤️  Здоровье: {self.player.health}/{self.player.max_health} HP")
        print(f"🚪 {room.get_description()}")
        print(f"==================================================")

        # Подготовка перед открытием двери (инвентарь / лут)
        self._preparation_phase(room)

        # Проверка запертых дверей
        if room.is_locked:
            if not self._handle_locked_door(room):
                self.handle_player_death("Ловушка запертой двери")
                return False

        # Спавн сущностей (Драш, Рейс и др.)
        for entity in self.entities:
            if entity.can_spawn(room):
                survived = entity.trigger(self.player, room)
                if not survived or not self.player.is_alive():
                    self.handle_player_death(entity.name)
                    return False
                break

        # Проверка ядовитого газа
        if room.is_gassed and self.player.is_alive():
            if not self._handle_gas_escape():
                self.handle_player_death("Отравление газом")
                return False

        return self.player.is_alive()

    def _preparation_phase(self, room):
        """Интерактивное меню действий перед выходом из комнаты."""
        while True:
            print("\nДействия:")
            print("1. Идти в следующую дверь")
            print("2. Открыть инвентарь")
            if room.loot_item:
                print("3. Осмотреть тумбочку / ящик")

            choice = input("Выберите действие (1-3): ").strip()

            if choice == "1":
                break
            elif choice == "2":
                self.player.show_inventory()
                if self.player.inventory:
                    idx = input("Номер предмета для использования (Enter - назад): ").strip()
                    if idx.isdigit():
                        self.player.use_item_by_index(int(idx) - 1, room)
            elif choice == "3" and room.loot_item:
                self.player.add_item(room.loot_item)
                room.loot_item = None
            else:
                print("❌ Неверный ввод.")

    def _handle_locked_door(self, room) -> bool:
        """Логика работы с запертыми дверями."""
        print("\n🔒 Дверь заперта!")
        has_lockpick = any(item.name == "Отмычки" for item in self.player.inventory)
        
        if has_lockpick:
            use_it = input("Применить Отмычки? (да/нет): ").strip().lower()
            if use_it == "да":
                for idx, item in enumerate(self.player.inventory):
                    if item.name == "Отмычки":
                        self.player.use_item_by_index(idx, room)
                        return True

        print("🔍 Вы тщательно осмотрели угол и нашли ключ на ящике!")
        room.is_locked = False
        return True

    def _handle_gas_escape(self) -> bool:
        """Реакция на ядовитый газ в комнате."""
        print("\n[☣️] ВНИМАНИЕ! Комнату быстро затягивает ядовитым газом!")
        start_time = time.time()
        input("СРОЧНО нажмите Enter, чтобы выскочить в дверь! ")
        elapsed = time.time() - start_time

        if elapsed > config.GAS_ESCAPE_TIME_LIMIT:
            damage = int((elapsed - config.GAS_ESCAPE_TIME_LIMIT) * 20) + 20
            print(f"[🤢] Задержка ({round(elapsed, 1)} сек)! Вы наглотались яда и получили {damage} урона!")
            self.player.take_damage(damage)
            return self.player.is_alive()
        
        print(f"[🏃] Вы вовремя выскочили из ядовитого облака за {round(elapsed, 1)} сек!")
        return True