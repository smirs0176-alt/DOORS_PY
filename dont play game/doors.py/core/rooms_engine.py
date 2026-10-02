import time
import random
from core.player import Player

class RoomsEngine:
    def __init__(self, player: Player):
        self.player = player
        self.current_room_number = 1  # Начинаем с A-001

    def start(self) -> bool:
        """Запуск прохождения The Rooms."""
        print("\n" + "⚙️" * 30)
        print("🚪 ВЫ СПУСТИЛИСЬ В THE ROOMS (Комната A-001)")
        print("💡 Здесь не работают обычные источники света.")
        print("⚠️ Будьте предельно внимательны к звукам!")
        print("⚙️" * 30)

        while self.player.is_alive():
            survived = self.play_turn()
            if not survived:
                return False

            if self.current_room_number >= 1000:
                print("\n🏆 ВЫ ПРОШЛИ ВСЕ 1000 КОМНАТ В THE ROOMS! ЭТО ЛЕГЕНДАРНО!")
                return True

        return False

    def play_turn(self) -> bool:
        """Логика одной комнаты A-XXX."""
        print(f"\n--------------------------------------------------")
        print(f"❤️  HP: {self.player.health}/{self.player.max_health} | 🚪 Комната A-{self.current_room_number:03d}")
        print(f"--------------------------------------------------")

        # Случайный спавн кастомных сущностей The Rooms
        if not self._check_entity_spawns():
            return False

        # Меню действий в комнате A-XXX
        print("\nДействия:")
        print("1. Идти дальше (открыть дверь)")
        print("2. Проверить инвентарь")
        
        choice = input("Выберите действие (1-2): ").strip()
        if choice == "2":
            self.player.show_inventory()

        self.current_room_number += 1
        return True

    def _check_entity_spawns(self) -> bool:
        """Спавн уникальных монстров The Rooms."""
        
        # 1. Спавн A-60 (Быстрый гул из глубины)
        if self.current_room_number > 60 and random.random() < 0.15:
            return self._trigger_a60()

        # 2. Спавн A-90 (Экранная помеха — нужно мгновенно ЗАМЕРЕТЬ)
        if self.current_room_number > 90 and random.random() < 0.12:
            return self._trigger_a90()

        # 3. Спавн A-120 (Гул спереди, возвращается несколько раз)
        if self.current_room_number > 120 and random.random() < 0.10:
            return self._trigger_a120()

        return True

    # --- МЕХАНИКИ МОНСТРОВ THE ROOMS ---

    def _trigger_a60(self) -> bool:
        print("\n📢 [ГЛУХОЙ ГУЛ] Откуда-то из дальних коридоров нарастает красный шум!")
        start_time = time.time()
        action = input("СРОЧНО! Введи 'шкаф', чтобы залезть в синий шкафчик: ").strip().lower()
        reaction = time.time() - start_time

        if action == "шкаф" and reaction <= 2.0:
            print("🔴 A-60 пролетел мимо шкафа с оглушительным красным сиянием!")
            return True
        else:
            print("💀 A-60 мгновенно стёр вас в порошок...")
            self.player.take_damage(100)
            return False

    def _trigger_a90(self) -> bool:
        print("\n🛑 [СТОП!] НА ЭКРАНЕ ПОЯВИЛСЯ ЗНАК A-90! НЕ ДВИГАЙСЯ!")
        start_time = time.time()
        action = input("Нажми Enter БЕЗ ВВОДА СИМВОЛОВ (просто замри): ")
        reaction = time.time() - start_time

        if action == "" and reaction <= 1.2:
            print("🙈 A-90 пролетел мимо, вас не заметили!")
            return True
        else:
            print("🛑 Вы дернулись! A-90 нанёс огромный урон!")
            self.player.take_damage(90)
            return self.player.is_alive()

    def _trigger_a120(self) -> bool:
        print("\n⚠️ [МЕДЛЕННЫЙ СТУК] A-120 приближается спереди... Он будет пролетать несколько раз!")
        
        for rebound in range(1, 3):
            start_time = time.time()
            action = input(f"[{rebound}/2] Быстро введи 'спрятаться': ").strip().lower()
            reaction = time.time() - start_time

            if action != "спрятаться" or reaction > 2.2:
                print("💀 A-120 настиг вас при возвращении...")
                self.player.take_damage(100)
                return False
            print(f"[✓] Пролёт {rebound} пережили!")

        print("✨ A-120 окончательно улетел обратно.")
        return True